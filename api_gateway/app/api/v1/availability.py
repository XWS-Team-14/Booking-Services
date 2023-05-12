from app.config import get_yaml_config
from fastapi import APIRouter, status
from fastapi.responses import Response
from fastapi_utils.cbv import cbv
from google.protobuf import json_format
import json
from loguru import logger
import grpc
from proto import availability_crud_pb2_grpc


router = APIRouter(
    tags=["Availability"],
)

@router.get(
    "/all",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all availabilities",
)
async def getAll():
    
    logger.info("Gateway processing getAll Availability request");
    availability_server = (
        get_yaml_config().get("availability_server").get("ip")
        + ":"
        + get_yaml_config().get("availability_server").get("port")
    )
    async with grpc.aio.insecure_channel(availability_server) as channel:
        stub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
        logger.info("Gateway processing getAll Availability data");
        data = await stub.GetAll({});
        json = json_format.MessageToJson(data)
    return Response(
        status_code=200, media_type="application/json", content=json
    )