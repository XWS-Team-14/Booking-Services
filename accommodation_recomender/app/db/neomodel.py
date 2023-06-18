from neomodel import config
from app.config import get_yaml_config
from loguru import logger

def get_neo4j_config():
    """
    Get Mongodb config in `config.yaml`
    :return:
    """
    config = get_yaml_config()
    return config.get("neo4j")

def start_neomodel():
    ip = get_neo4j_config().get("ip")
    port = get_neo4j_config().get("port")
    username = get_neo4j_config().get("username")
    password = get_neo4j_config().get("password")
    db = get_neo4j_config().get("db")
    config.DATABASE_URL = (f'bolt://{username}:{password}@{ip}:{port}')
    logger.info(f"Set neomodel config database_url {config.DATABASE_URL}")
    