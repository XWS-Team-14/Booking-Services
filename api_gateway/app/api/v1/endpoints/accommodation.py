import httpx
import asyncio
from uuid import uuid4
from fastapi import APIRouter, File
from fastapi.responses import HTMLResponse, Response
from app.config import get_yaml_config
from typing import Annotated

router = APIRouter()


@router.post("/", response_class=HTMLResponse)
async def save_image(
    # Add additional data that needs to be here
    files: Annotated[list[bytes], File()]
):
    image_uris = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for file in files:
            url = get_yaml_config().get("static_server").get("url")
            sending_file = file
            file_type = get_yaml_config().get("static_server").get("image_file_type")
            image_uri = uuid4() + file_type
            image_uris.append(image_uri)
            data = {"image_uri": image_uri}
            tasks.append(
                asyncio.ensure_future(client.post(url, data=data, files=sending_file))
            )
        # Might be good to check if every image was saved properly
        await asyncio.gather(*tasks)
    # Send grpc request to save accommodation data
    return Response(
        status_code=200, media_type="text/html", content="Accommodation saved!"
    )
