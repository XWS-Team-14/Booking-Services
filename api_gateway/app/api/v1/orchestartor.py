import grpc
from fastapi import APIRouter, status, Cookie
from fastapi.responses import Response
import uuid
from api_gateway.app.schemas.orchestrator import UserId
from proto import orchestrator_pb2,orchestrator_pb2_grpc
from ...constants import orchestrator_server

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
    async with grpc.aio.insecure_channel(orchestrator_server) as channel:
        stub = orchestrator_pb2_grpc.OrchestratorCrudStub(channel)
        data = await stub.Delete(orchestrator_pb2.UserId(user_id=user_id))
    return Response(status_code=data.error_message, media_type="application/json", content=data.error_code)