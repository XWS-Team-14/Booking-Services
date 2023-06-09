import asyncio
import json
from typing import Annotated, List
from uuid import uuid4

import grpc
import httpx
from app.schemas.accommodation import (
    Accommodation,
    Location,
    ResponseAccommodation,
    ResponseAccommodations,
)
from app.utils.json_encoder import UUIDEncoder
from fastapi import APIRouter, Cookie, Form, UploadFile
from fastapi.responses import HTMLResponse, ORJSONResponse, Response
from google.protobuf.json_format import MessageToDict, Parse, MessageToJson
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger

from proto import (
    accommodation_pb2,
    accommodation_pb2_grpc,
    reservation_crud_pb2,
    reservation_crud_pb2_grpc,
review_pb2_grpc, review_pb2
)

from ...config import get_yaml_config
from ...constants import accommodation_server, reservation_server, review_server
from ...utils.get_server import get_server
from ...utils.jwt import get_id_from_token, get_role_from_token
from opentelemetry.instrumentation.grpc import aio_client_interceptors

router = APIRouter()


@router.post("/", response_class=HTMLResponse)
async def save_accommodation(
        # Add additional data that needs to be here
        access_token: Annotated[str | None, Cookie()],
        name: Annotated[str, Form()],
        country: Annotated[str, Form()],
        city: Annotated[str, Form()],
        address: Annotated[str, Form()],
        auto_accept_flag: Annotated[str, Form()],
        min_guests: Annotated[int, Form()],
        max_guests: Annotated[int, Form()],
        features: Annotated[List[str], Form()],
        files: List[UploadFile],
):
    """Post method used to save acoommodation

    It saves images with their unique ID and then sends gRPC request to
    accommodation service to save data about accommodation
    """

    try:
        user_id = get_id_from_token(access_token)
        user_role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if user_role != "host":
        return Response(status_code=401, media_type="text/html", content="Unauthorized")
    image_uris = []
    async with httpx.AsyncClient() as client:
        tasks = []
        if len(files) > 0:
            for file in files:
                content = file.file.read()
                url = get_yaml_config().get("static_server").get("url")
                sending_file = {"file": content}
                file_type = (
                    get_yaml_config().get("static_server").get("image_file_type")
                )
                image_uri = str(uuid4()) + file_type
                image_uris.append(image_uri)
                data = {"image_uri": image_uri}
                tasks.append(
                    asyncio.ensure_future(
                        client.post(url, data=data, files=sending_file)
                    )
                )
            # Might be good to check if every image was saved properly
            await asyncio.gather(*tasks)
    # Send grpc request to save accommodation data
    async with grpc.aio.insecure_channel(accommodation_server, interceptors=aio_client_interceptors()) as channel:
        stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)

        location = Location(
            country=country,
            city=city,
            address=address,
        )
        features_list = []
        image_urls_list = []

        for item in features:
            for i in item.split(","):
                features_list.append(i)
        for item in image_uris:
            image_urls_list.append(item)

        accommodation = Accommodation(
            id=str(uuid4()),
            host_id=user_id,
            name=name,
            location=location,
            features=features_list,
            image_urls=image_urls_list,
            min_guests=int(min_guests),
            max_guests=int(max_guests),
            auto_accept_flag=auto_accept_flag,
        )

        response = await stub.Create(
            Parse(
                json.dumps(accommodation.dict(), cls=UUIDEncoder),
                accommodation_pb2.Accommodation(),
            )
        )
    async with grpc.aio.insecure_channel(reservation_server, interceptors=aio_client_interceptors()) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        await stub.CreateAccommodation(
            reservation_crud_pb2.AccommodationResDto(
                id=str(accommodation.id), automaticAccept=True if auto_accept_flag == 'true' else False
            )
        )

    async with grpc.aio.insecure_channel(review_server, interceptors=aio_client_interceptors()) as channel:
        stub = review_pb2_grpc.ReviewServiceStub(channel)
        await stub.CreateHostAndAccommodation(
            review_pb2.HostAccommodation(
                host_id=str(user_id),
                accommodation_id=str(accommodation.id)
            )
        )
    return Response(
        status_code=response.status_code,
        media_type="text/html",
        content=response.message_string,
    )


@router.get("/allByUser")
async def GetByUserId(access_token: Annotated[str | None, Cookie()] = None):
    try:
        user_id = get_id_from_token(access_token)
        user_role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if user_role != "host":
        return Response(status_code=401, media_type="text/html", content="Unauthorized")

    async with grpc.aio.insecure_channel(accommodation_server, interceptors=aio_client_interceptors()) as channel:
        stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)
        dto = accommodation_pb2.InputId(
            id=user_id,
        )
        response = await stub.GetByUser(dto)

    parsed_response = ResponseAccommodations.parse_obj(
        MessageToDict(response, preserving_proto_field_name=True)
    )
    # fix paths for image_urls
    updated_url = "http://localhost:8888/api/static/images/"
    try:
        for item in parsed_response.items:
            updated_urls = []
            for img_url in item.image_urls:
                updated_urls.append(updated_url + img_url)
            item.image_urls = updated_urls
    except Exception as e:
        logger.error(f"Error {e}")
    return ORJSONResponse(
        status_code=parsed_response.response.status_code,
        content=parsed_response.dict(),
    )


@router.get("/all")
async def getAll():
    logger.info("Gateway processing getAll reservations")
    async with grpc.aio.insecure_channel(accommodation_server, interceptors=aio_client_interceptors()) as channel:
        stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)
        logger.info("Gateway processing getAll reservation data")
        data = await stub.GetAll({})

    parsed_response = ResponseAccommodations.parse_obj(
        MessageToDict(data, preserving_proto_field_name=True)
    )
    # fix paths for image_urls
    updated_url = "http://localhost:8888/api/static/images/"
    try:
        for item in parsed_response.items:
            updated_urls = []
            for img_url in item.image_urls:
                updated_urls.append(updated_url + img_url)
            item.image_urls = updated_urls
    except Exception as e:
        logger.error(f"Error {e}")
    return ORJSONResponse(
        status_code=parsed_response.response.status_code,
        content=parsed_response.dict(),
    )


@router.get("/id/{item_id}")
async def GetById(item_id):
    async with grpc.aio.insecure_channel(accommodation_server, interceptors=aio_client_interceptors()) as channel:
        stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)

        response = await stub.GetById(accommodation_pb2.InputId(id=item_id))

    parsed_response = ResponseAccommodation.parse_obj(
        MessageToDict(response, preserving_proto_field_name=True)
    )
    if response.item.id == "":
        return Response(
            status_code=200, media_type="application/json", content="Invalid id"
        )
    updated_url = "http://localhost:8888/api/static/images/"
    try:
        updated_urls = []
        for img_url in parsed_response.item.image_urls:
            updated_urls.append(updated_url + img_url)
        parsed_response.item.image_urls = updated_urls
    except Exception as e:
        logger.error(f"Error {e}")

    return ORJSONResponse(
        status_code=parsed_response.response.status_code,
        content=parsed_response.dict(),
    )


@router.get("/amenities")
async def get_all_amenities():
    async with grpc.aio.insecure_channel(accommodation_server, interceptors=aio_client_interceptors()) as channel:
        stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)
        logger.info("Gateway processing get all amenities")
        data = await stub.GetAllAmenities({})

    return Response(status_code=200, content=MessageToJson(data))
