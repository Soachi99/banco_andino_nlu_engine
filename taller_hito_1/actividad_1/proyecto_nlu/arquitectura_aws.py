"""Arquitectura AWS tentativa del motor NLU. Genera arquitectura_nlu_aws.png.

El recorrido de una solicitud sigue los diagramas de secuencia e identidades:
React solo llega a la API, la API solo al coordinador, y los agentes no se llaman
entre sí. Bedrock lo usan intérprete, extractor y análisis. El validador no.
REMITIR_PROCESO sale por EventBridge y DERIVAR_OPERADOR por SQS.
SOLICITAR_INFORMACION vuelve en la misma respuesta HTTP.
"""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Fargate
from diagrams.aws.database import Aurora
from diagrams.aws.general import General, Users
from diagrams.aws.integration import Eventbridge, SQS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.ml import Bedrock
from diagrams.aws.network import APIGateway, CloudFront, Route53
from diagrams.aws.security import Cognito, WAF
from diagrams.aws.storage import S3

graph_attr = {
    "pad": "0.45",
    "splines": "spline",
    "nodesep": "0.55",
    "ranksep": "0.85",
    "fontsize": "16",
    "bgcolor": "white",
    "fontname": "Segoe UI",
    "compound": "true",
}
node_attr = {"fontname": "Segoe UI", "fontsize": "12"}
edge_attr = {"fontname": "Segoe UI", "fontsize": "11"}

with Diagram(
    "Motor NLU en AWS — arquitectura tentativa",
    filename=str(Path(__file__).with_name("arquitectura_nlu_aws")),
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
):
    cliente = Users("Cliente")
    operador = Users("Operador")
    proceso = General("Siguiente\nproceso de negocio")

    with Cluster("Borde", graph_attr={"bgcolor": "#EFF6FF"}):
        dns = Route53("Route 53")
        waf = WAF("WAF")
        cdn = CloudFront("CloudFront")
        spa = S3("S3\nReact")
        apigw = APIGateway("API Gateway\nPOST /api/solicitudes")
        auth = Cognito("Cognito\ncliente")

    with Cluster("VPC privada", graph_attr={"bgcolor": "#F8FAFC"}):
        with Cluster("ECS Fargate", graph_attr={"bgcolor": "#FFFFFF"}):
            api = Fargate("API de solicitudes\nNode")
            coord = Fargate("Coordinador")

            with Cluster("Comprensión", graph_attr={"bgcolor": "#F0FDF4"}):
                interprete = Fargate("Intérprete")
                extractor = Fargate("Extractor")
                analisis = Fargate("Análisis\ncontextual")

            with Cluster("Control", graph_attr={"bgcolor": "#FFFBEB"}):
                validador = Fargate("Validador\nreglas del caso")

        solicitudes = Aurora("Aurora PostgreSQL\nestado de la solicitud")

    modelo = Bedrock("Bedrock\nintención, datos y resumen")
    bus = Eventbridge("EventBridge\nsolicitud remitida")
    cola = SQS("SQS\ncaso derivado")
    logs = Cloudwatch("CloudWatch\nlogs y trazas")

    cliente >> dns >> waf >> cdn
    cdn >> spa
    cdn >> Edge(label="/api/*") >> apigw
    apigw >> Edge(label="autoriza") >> auth
    apigw >> Edge(label="VPC Link") >> api

    api >> Edge(label="estado") >> solicitudes
    api >> Edge(label="analizar(mensaje)") >> coord

    coord >> Edge(label="en paralelo", color="#166534") >> interprete
    coord >> Edge(label="en paralelo", color="#166534") >> extractor
    coord >> Edge(label="después", color="#166534") >> analisis
    coord >> Edge(label="validar", color="#A16207") >> validador

    interprete >> Edge(color="#166534") >> modelo
    extractor >> Edge(color="#166534") >> modelo
    analisis >> Edge(color="#166534") >> modelo

    coord >> Edge(label="REMITIR_PROCESO", color="#C2410C") >> bus >> proceso
    coord >> Edge(label="DERIVAR_OPERADOR", color="#9D174D") >> cola >> operador

    [api, coord] >> Edge(style="dashed", color="#64748B") >> logs
