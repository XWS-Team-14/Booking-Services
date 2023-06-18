import grpc
from fastapi import APIRouter, status, Cookie
from fastapi.responses import Response
import uuid
from proto import orchestrator_pb2,orchestrator_pb2_grpc
from ...constants import orchestrator_server
from loguru import logger
from opentelemetry.instrumentation.grpc import aio_client_interceptors

router = APIRouter(
    tags=["Orchestrator"],
)

@router.delete(
    "/delete/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete User via SAGA",
)
async def deleteUser(user_id):
    logger.info("Gateway processing delete user via saga request")
    async with grpc.aio.insecure_channel(orchestrator_server, interceptors=aio_client_interceptors()) as channel:
        stub = orchestrator_pb2_grpc.OrchestratorStub(channel)
        data = await stub.DeleteUser(orchestrator_pb2.UserId(id=user_id))
        logger.info(data)
        logger.info(data.error_message)
        logger.info(data.error_code)
    return Response(status_code=data.error_code, media_type="text/html", content=data.error_message)
