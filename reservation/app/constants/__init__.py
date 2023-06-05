from app.config import get_yaml_config

kafka_server = get_yaml_config().get("kafka_server").get("ip") + ":" + get_yaml_config().get("kafka_server").get("port")
