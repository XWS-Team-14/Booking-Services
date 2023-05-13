import sys
import urllib.parse
from typing import Optional

from beanie import init_beanie
from loguru import logger
from motor.core import AgnosticClient
from motor.core import AgnosticCollection
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_yaml_config
from app.models.accommodation import Accommodation

async_mongodb_client = None


def get_mongodb_config():
    """
    Get Mongodb config in `config.yaml`
    :return:
    """
    config = get_yaml_config()
    return config.get("mongodb")


def get_async_mongodb_client() -> AgnosticClient:
    """
    Raw Motor client handler, use it when beanie cannot work
    :return:
    """
    global async_mongodb_client
    if async_mongodb_client is None:
        ip = get_mongodb_config().get("ip")
        port = get_mongodb_config().get("port")
        username = urllib.parse.quote_plus(get_mongodb_config().get("username"))
        password = urllib.parse.quote_plus(get_mongodb_config().get("password"))
        async_mongodb_client = AsyncIOMotorClient(
            f"mongodb://{username}:{password}@{ip}:{port}",
            serverSelectionTimeoutMS=10000
        )
    return async_mongodb_client


def get_async_mongodb_database(db_name: Optional[str]) -> AgnosticDatabase:
    """
    Raw Motor database handler, use it when beanie cannot work
    :param db_name:
    :return:
    """
    if db_name is None:
        db_name = get_mongodb_config().get("db")
    client = get_async_mongodb_client()

    return client[db_name]


def get_async_mongodb_collection(col_name: str) -> AgnosticCollection:
    """
    Raw Motor collection handler, use it when beanie cannot work
    :param col_name:
    :return:
    """
    db = get_async_mongodb_database(None)
    return db[col_name]


async def start_async_mongodb() -> None:
    """
    Start beanie when process started.
    :return:
    """
    try:
        async_mongodb_database = get_async_mongodb_database(None)
        await init_beanie(
            database=async_mongodb_database,
            document_models=[
                Accommodation
            ],
        )
        logger.success("Started mongodb connection")
    except Exception as e:
        logger.exception(f"Failed to start mongodb. error={e}")
        sys.exit(1)
