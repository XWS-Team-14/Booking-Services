import json

from kafka import KafkaProducer, KafkaConsumer

from app.utils import get_server

JWT_ACCESS_SECRET = "2bcb77e4-c775-4070-a2fa-bfa5f3e020a0"
JWT_REFRESH_SECRET = "2a8590e5-6689-4108-bea6-c6983896504f"

kafka_server = get_server("kafka_server")
user_server = get_server("user_server")
auth_server = get_server("auth_server")
reservation_server = get_server("reservation_server")
availability_server = get_server("availability_server")
accommodation_server = get_server("accommodation_server")
search_server = get_server("search_server")
notification_server = get_server("notification_server")
review_server = get_server("review_server")
orchestrator_server = get_server("orchestrator_server")
accommodation_recomender_server = get_server("recomdender_server")
airline_server = "http://" + get_server("airline_server")

kafka_producer = KafkaProducer(bootstrap_servers=[kafka_server], value_serializer=lambda m: json.dumps(m).encode('ascii'))
