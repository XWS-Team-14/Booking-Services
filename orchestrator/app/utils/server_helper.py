from app.config import get_yaml_config


def get_server(server_name: str):
    return get_yaml_config().get(server_name).get("ip") + ":" + get_yaml_config().get(server_name).get("port")
