import grpc
from fastapi import APIRouter, status, Cookie
from fastapi.responses import Response, JSONResponse
import uuid
from proto import accommodation_recomender_pb2, accommodation_recomender_pb2_grpc
from ...constants import accommodation_recomender_server, accommodation_server
from loguru import logger
from google.protobuf import json_format
from google.protobuf.json_format import MessageToDict
from proto import (
    accommodation_pb2,
    accommodation_pb2_grpc
)
import json
from app.schemas.accommodation import (
    Accommodation,
    Location,
    ResponseAccommodation,
    ResponseAccommodations,
)
from opentelemetry.instrumentation.grpc import aio_client_interceptors

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
    async with grpc.aio.insecure_channel(accommodation_recomender_server, interceptors=aio_client_interceptors()) as channel:
        stub = accommodation_recomender_pb2_grpc.AccommodationRecomenderStub(channel)
        data = await stub.GetRecomended(accommodation_recomender_pb2.User_id(id=user_id))
        if data.ids[0] == '':
            logger.info("None found returning error")
            return Response(
                status_code=404, media_type="text/html", content='Error: None found'
            ) 
    retVal=[]
    logger.info("Fetched accommodation ids processing to whole objects")
    async with grpc.aio.insecure_channel(accommodation_server, interceptors=aio_client_interceptors()) as channel:
        stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)

        for accommodation_id in data.ids:
            response = await stub.GetById(accommodation_pb2.InputId(id=accommodation_id))

            parsed_response = ResponseAccommodation.parse_obj(
                MessageToDict(response, preserving_proto_field_name=True)
            )
            logger.info(parsed_response)
            if response.item.id == "":
                continue
            updated_url = "http://localhost:8000/api/static/images/"
            try:
                updated_urls = []
                for img_url in parsed_response.item.image_urls:
                    updated_urls.append(updated_url + img_url)
                parsed_response.item.image_urls = updated_urls
            except Exception as e:
                logger.error(f"Error {e}")
            if parsed_response.response.status_code == 200:
                parsed_response.item.id = str(parsed_response.item.id)
                parsed_response.item.host_id = str(parsed_response.item.host_id)
                retVal.append(parsed_response.item.dict())
    logger.info("Processing complete returning list of accommodataions")  
    
    return Response(
        status_code=200, media_type="application/json", content=json.dumps(retVal)
    )
