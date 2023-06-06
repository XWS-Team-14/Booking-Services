import json

from kafka import KafkaConsumer

from app.config import get_yaml_config

kafka_server = get_yaml_config().get("kafka_server").get("ip") + ":" + get_yaml_config().get("kafka_server").get("port")
kafka_consumer = KafkaConsumer('reservations',
                               group_id='reservations',
                               bootstrap_servers=[kafka_server],
                               value_deserializer=lambda m: json.loads(m.decode('ascii'))
                               )
