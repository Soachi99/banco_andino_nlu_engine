"""Arquitectura AWS de una app de transporte. Genera arquitectura_transporte_aws.png."""

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.compute import ECR, Fargate
from diagrams.aws.database import Aurora, Dynamodb, ElasticacheForRedis
from diagrams.aws.engagement import Pinpoint
from diagrams.aws.general import General, Users
from diagrams.aws.integration import Eventbridge, SNS, SQS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import ALB, APIGateway, CloudFront, Route53
from diagrams.aws.security import Cognito, SecretsManager, WAF
from diagrams.aws.storage import S3

with Diagram(
    "App de transporte en AWS",
    filename="arquitectura_transporte_aws",
    show=False,
    direction="TB",
    graph_attr={"pad": "0.5", "splines": "spline", "nodesep": "0.6"},
):
    usuarios = Users("Apps pasajero y conductor")

    with Cluster("Borde"):
        dns = Route53("Route 53")
        cdn = CloudFront("CloudFront")
        waf = WAF("WAF")
        api = APIGateway("API Gateway")
        auth = Cognito("Cognito")

    with Cluster("VPC"):
        alb = ALB("ALB")

        with Cluster("ECS en Fargate"):
            viajes = Fargate("Viajes")
            matching = Fargate("Matching")
            tracking = Fargate("Tracking")
            pagos = Fargate("Pagos")
            notif = Fargate("Notificaciones")

        with Cluster("Datos"):
            aurora = Aurora("Aurora PostgreSQL\nviajes y usuarios")
            estado = Dynamodb("DynamoDB\nestado en vivo")
            redis = ElasticacheForRedis("Redis\nconductores cercanos")

        with Cluster("Eventos"):
            gps = KinesisDataStreams("Kinesis\nposiciones")
            ofertas = SQS("SQS\nofertas de viaje")
            bus = Eventbridge("EventBridge")
            push = SNS("SNS")

    recibos = S3("S3\nrecibos y media")
    imagenes = ECR("ECR")
    secretos = SecretsManager("Secrets Manager")
    observabilidad = Cloudwatch("CloudWatch")
    avisos = Pinpoint("Pinpoint")
    pasarela = General("Pasarela de pago")

    usuarios >> dns >> waf >> api
    api >> auth
    api >> Edge(label="VPC Link") >> alb
    alb >> [viajes, matching, tracking, pagos]

    cdn >> recibos
    imagenes >> [viajes, matching, tracking, pagos, notif]

    # El conductor publica GPS; matching elige con el índice geo.
    tracking >> gps >> matching
    matching >> redis
    matching >> Edge(label="oferta") >> ofertas >> viajes

    viajes >> [aurora, estado]
    viajes >> Edge(label="aceptado / finalizado") >> bus
    bus >> notif >> push >> avisos >> usuarios

    # Al cerrar el viaje se cobra y se guarda el recibo.
    viajes >> Edge(label="tarifa") >> pagos
    pagos >> secretos
    pagos >> pasarela
    pagos >> recibos

    [viajes, matching, tracking, pagos] >> observabilidad