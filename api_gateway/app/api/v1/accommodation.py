import httpx
import asyncio
import grpc
import json
from uuid import uuid4
from fastapi import APIRouter, Form, UploadFile, Cookie
from fastapi.responses import HTMLResponse, Response
from app.config import get_yaml_config
from typing import Annotated, List
from types import SimpleNamespace
from jwt import ExpiredSignatureError, InvalidTokenError
from proto import accommodation_crud_pb2_grpc
from proto import accommodation_crud_pb2
from google.protobuf.json_format import MessageToJson
from loguru import logger
from app.utils.jwt import get_id_from_token, get_role_from_token

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
    accommodation_server = (
        get_yaml_config().get("accommodation_server").get("ip")
        + ":"
        + get_yaml_config().get("accommodation_server").get("port")
    )
    async with grpc.aio.insecure_channel(accommodation_server) as channel:
        stub = accommodation_crud_pb2_grpc.AccommodationCrudStub(channel)

        location = accommodation_crud_pb2.Location(
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

        accommodation = accommodation_crud_pb2.Accommodation(
            id=str(uuid4()),
            user_id=user_id,
            name=name,
            location=location,
            features=features_list,
            image_urls=image_urls_list,
            min_guests=int(min_guests),
            max_guests=int(max_guests),
            auto_accept_flag=auto_accept_flag,
        )

        await stub.Create(accommodation)

    return Response(
        status_code=200, media_type="text/html", content="Accommodation saved!"
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

    accommodation_server = (
        get_yaml_config().get("accommodation_server").get("ip")
        + ":"
        + get_yaml_config().get("accommodation_server").get("port")
    )

    async with grpc.aio.insecure_channel(accommodation_server) as channel:
        stub = accommodation_crud_pb2_grpc.AccommodationCrudStub(channel)
        dto = accommodation_crud_pb2.DtoId(
            id=user_id,
        )
        response = await stub.GetByUser(dto)

    res = json.loads(
        MessageToJson(response), object_hook=lambda d: SimpleNamespace(**d)
    )
    # fix paths for image_urls
    updated_url = "http://localhost:8000/api/static/images/"
    try:
        for item in res.items:
            updated_urls = []
            for img_url in item.imageUrls:
                updated_urls.append(updated_url + img_url)
            item.imageUrls = updated_urls
    except Exception as e:
        logger.error(f"Error {e}")
    return res
