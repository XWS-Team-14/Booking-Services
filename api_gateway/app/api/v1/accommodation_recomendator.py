import grpc
from fastapi import APIRouter, status, Cookie
from fastapi.responses import Response
import uuid
from proto import accommodation_recomender_pb2, accommodation_recomender_pb2_grpc
from ...constants import accommodation_recomender_server
from loguru import logger

router = APIRouter(
    tags=["Accommodation_recomender"],
)

@router.get(
    "/get/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get reccomended accomodations for user_id",
)
async def getRecomdendations(user_id):
    logger.info("Gateway processing get accommodation recomnedations request")
    async with grpc.aio.insecure_channel(accommodation_recomender_server) as channel:
        stub = accommodation_recomender_pb2_grpc.AccommodationRecomenderStub(channel)
        data = await stub.GetRecomended(accommodation_recomender_pb2.User_id(id=user_id))
        logger.info(data)

    return Response(status_code=200, media_type="text/html", content=data.ids)