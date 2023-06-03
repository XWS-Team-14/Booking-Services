import io
import os
from typing import Annotated
from fastapi.responses import FileResponse, HTMLResponse, Response
from PIL import Image
from fastapi import APIRouter, File, Form
from loguru import logger
from app.config import get_yaml_config
from app.schemas import response

router = APIRouter()


@router.get("/{image_uri}", response_class=FileResponse)
async def get_image(image_uri: str):
    # Retrive image using PIL
    full_image_path = os.path.join(
        os.sep.join(get_yaml_config().get("app").get("image_resources_location")),
        image_uri,
    )

    try:
        image = Image.open(full_image_path)
    except FileNotFoundError as e:
        logger.critical(f"{e}: Image does not exist! PATH: {full_image_path}")
        return Response(status_code=400, media_type="text/html", content=f"{e}")
    # Create a response with the appropriate content type
    img_io = io.BytesIO()
    image.save(img_io, format="PNG")
    img_io.seek(0)
    return Response(content=img_io.getvalue(), media_type="image/jpeg")


@router.post("/", response_class=HTMLResponse)
async def save_image(file: Annotated[bytes, File()], image_uri: Annotated[str, Form()]):
    full_image_path = os.path.join(
        os.sep.join(get_yaml_config().get("app").get("image_resources_location")),
        image_uri,
    )
    logger.info(f"Saving image. PATH: {full_image_path}")
    res = response.Response.construct()
    try:
        image = Image.open(io.BytesIO(file))
        image.save(full_image_path)
    except Exception as e:
        logger.critical(f"{e}: Error! PATH: {full_image_path}")
        res.message_string = e
        res.status_code = 400
    else:
        logger.success(f"Image saved! PATH: {full_image_path}")
        res.message_string = "Image saved!"
        res.status_code = 200
    return Response(
        status_code=res.status_code, media_type="text/html", content=res.message_string
    )


@router.delete("/", response_class=HTMLResponse)
async def delete_image(image_uri: str):
    full_image_path = os.path.join(
        os.sep.join(get_yaml_config().get("app").get("image_resources_location")),
        image_uri,
    )
    logger.info(f"Deleting image. PATH: {full_image_path}")
    res = response.Response.construct()
    try:
        os.remove(full_image_path)
    except FileNotFoundError as e:
        logger.critical(f"{e}: Error! PATH: {full_image_path}")
        res.message_string = e
        res.status_code = 400
    else:
        logger.success(f"Image deleted! PATH: {full_image_path}")
        res.message_string = "Image deleted!"
        res.status_code = 200
    return Response(
        status_code=res.status_code, media_type="text/html", content=res.message_string
    )
