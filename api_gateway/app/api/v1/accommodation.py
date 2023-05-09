import httpx
import asyncio
import grpc
from uuid import uuid4
from fastapi import APIRouter, File
from fastapi.responses import HTMLResponse, Response
from app.config import get_yaml_config
from typing import Annotated

from proto import accommodation_crud_pb2_grpc
from proto import accommodation_crud_pb2

router = APIRouter()


@router.post("/", response_class=HTMLResponse)
async def save_accommodation(
    # Add additional data that needs to be here
    files: Annotated[list[bytes], File()]
):
    """Post method used to save acoommodation

    It saves images with their unique ID and then sends gRPC request to
    accommodation service to save data about accommodation
    """
    image_uris = []
    async with httpx.AsyncClient() as client:
        tasks = []
        if len(files) > 0:
            for file in files:
                url = get_yaml_config().get("static_server").get("url")
                sending_file = {"file": file}
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
        await stub.Delete(accommodation_crud_pb2.AccommodationId(id="15"))
    return Response(
        status_code=200, media_type="text/html", content="Accommodation saved!"
    )
