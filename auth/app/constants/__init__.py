JWT_ACCESS_SECRET = "2bcb77e4-c775-4070-a2fa-bfa5f3e020a0"
JWT_REFRESH_SECRET = "2a8590e5-6689-4108-bea6-c6983896504f"

import json

from kafka import KafkaProducer

from app.config import get_yaml_config

from opentelemetry.instrumentation.kafka import KafkaInstrumentor
KafkaInstrumentor().instrument()

kafka_server = get_yaml_config().get("kafka_server").get("ip") + ":" + get_yaml_config().get("kafka_server").get("port")
kafka_producer = KafkaProducer(bootstrap_servers=[kafka_server],
                               value_serializer=lambda m: json.dumps(m).encode('ascii'))
