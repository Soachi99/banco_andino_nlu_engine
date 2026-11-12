
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.mobile import Mobile
from diagrams.aws.network import (
    Route53,
    CloudFront,
    APIGateway,
)
from diagrams.aws.security import Cognito, WAF
from diagrams.aws.compute import Lambda
from diagrams.aws.database import (
    Dynamodb,
    Elasticache,
    RDS,
)
from diagrams.aws.integration import (
    Eventbridge,
    SQS,
    SNS,
)
from diagrams.aws.storage import S3
from diagrams.aws.devtools import XRay
from diagrams.aws.management import Cloudwatch
from diagrams.generic.blank import Blank


graph_attr = {
    "fontsize": "20",
    "bgcolor": "white",
    "pad": "0.5",
    "splines": "spline",
    "nodesep": "0.7",
    "ranksep": "1.0",
    "fontname": "Arial"
}

with Diagram(
    "Uber - AWS Cloud Architecture",
    filename="uber_aws_architecture",
    outformat="png",
    show=False,
    direction="LR",
    graph_attr=graph_attr
):

    # ==========================================
    # CLIENT APPLICATIONS
    # ==========================================

    with Cluster("Mobile Applications - Flutter"):
        passenger = Mobile("Passenger App")
        driver = Mobile("Driver App")

    # ==========================================
    # AWS EDGE AND API
    # ==========================================

    with Cluster("AWS - Edge & Security"):

        dns = Route53("Route 53")
        cdn = CloudFront("CloudFront")
        waf = WAF("AWS WAF")

        with Cluster("API Layer"):
            api = APIGateway("REST API")
            websocket = APIGateway("WebSocket API")
            auth = Cognito("Amazon Cognito")

    # ==========================================
    # BUSINESS SERVICES
    # ==========================================

    with Cluster("AWS - Application Services"):

        with Cluster("Ride Management"):
            ride_service = Lambda("Ride Service")
            pricing_service = Lambda("Pricing Service")
            matching_service = Lambda("Driver Matching")

        with Cluster("Driver Management"):
            location_service = Lambda("Location Service")
            driver_service = Lambda("Driver Service")

        with Cluster("Payments"):
            payment_service = Lambda("Payment Service")

        with Cluster("Notifications"):
            notification_service = Lambda("Notification Service")

    # ==========================================
    # DATA LAYER
    # ==========================================

    with Cluster("AWS - Data Layer"):

        ride_db = RDS("Aurora PostgreSQL")

        driver_db = Dynamodb("Driver Data")

        location_cache = Elasticache(
            "Redis Geospatial Cache"
        )

        storage = S3("S3 - Receipts & Files")

    # ==========================================
    # EVENT-DRIVEN ARCHITECTURE
    # ==========================================

    with Cluster("AWS - Event Processing"):

        event_bus = Eventbridge("EventBridge")

        ride_queue = SQS("Ride Events Queue")

        notification_queue = SQS(
            "Notification Queue"
        )

        sns = SNS("Push Notifications")

    # ==========================================
    # EXTERNAL SERVICES
    # ==========================================

    with Cluster("External Integrations"):
        payment_gateway = Blank("Payment Provider")
        push_provider = Blank("FCM / APNs")

    # ==========================================
    # OBSERVABILITY
    # ==========================================

    with Cluster("AWS - Observability"):
        monitoring = Cloudwatch("CloudWatch")
        tracing = XRay("AWS X-Ray")

    # ==========================================
    # CLIENT -> EDGE
    # ==========================================

    passenger >> dns
    driver >> dns

    dns >> cdn >> waf >> api

    # Real-time communication
    passenger >> Edge(style="dashed") >> websocket
    driver >> Edge(style="dashed") >> websocket

    # Authentication
    auth >> Edge(style="dashed", label="JWT validation") >> api

    # ==========================================
    # API -> BUSINESS SERVICES
    # ==========================================

    api >> ride_service
    api >> pricing_service
    api >> location_service
    api >> driver_service
    api >> payment_service

    # Ride orchestration
    ride_service >> pricing_service
    ride_service >> matching_service

    # Driver management
    location_service >> location_cache
    location_service >> driver_db

    matching_service >> location_cache
    matching_service >> driver_db

    driver_service >> driver_db

    # ==========================================
    # PERSISTENCE
    # ==========================================

    ride_service >> ride_db
    payment_service >> ride_db

    payment_service >> storage

    # ==========================================
    # EVENT-DRIVEN COMMUNICATION
    # ==========================================

    ride_service >> event_bus
    matching_service >> event_bus
    payment_service >> event_bus

    event_bus >> ride_queue
    event_bus >> notification_queue

    notification_queue >> notification_service
    notification_service >> sns
    sns >> push_provider

    # Real-time updates
    ride_service >> Edge(
        style="dashed",
        label="Trip status"
    ) >> websocket

    websocket >> passenger
    websocket >> driver

    # ==========================================
    # EXTERNAL PAYMENT
    # ==========================================

    payment_service >> payment_gateway

    # ==========================================
    # MONITORING AND TRACING
    # ==========================================

    for service in [
        ride_service,
        pricing_service,
        matching_service,
        location_service,
        driver_service,
        payment_service,
        notification_service
    ]:
        service >> Edge(
            style="dotted",
            color="gray"
        ) >> monitoring

        service >> Edge(
            style="dotted",
            color="gray"
        ) >> tracing

print("Architecture diagram generated successfully!")
