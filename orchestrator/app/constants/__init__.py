import json

from app.utils.server_helper import get_server
from kafka import KafkaProducer
from app.config import get_yaml_config

from opentelemetry.instrumentation.kafka import KafkaInstrumentor
KafkaInstrumentor().instrument()

kafka_server = get_yaml_config().get("kafka_server").get("ip") + ":" + get_yaml_config().get("kafka_server").get("port")
kafka_producer = KafkaProducer(bootstrap_servers=[kafka_server],
                               value_serializer=lambda m: json.dumps(m).encode('ascii'))

accommodation_server = get_server("accommodation_server")
