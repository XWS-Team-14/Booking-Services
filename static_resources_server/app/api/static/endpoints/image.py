import io
import os
from typing import Annotated
from fastapi.responses import FileResponse, HTMLResponse, ORJSONResponse, Response
from PIL import Image
from fastapi import APIRouter, UploadFile, File, Form
from fastapi_utils.cbv import cbv
from loguru import logger
from app.config import get_yaml_config
from app import schemas

router = APIRouter()


@router.get("/{image_uri}",
            response_class=FileResponse)
async def get_image(image_uri: str):
    # Retrive image using PIL
    full_image_path = os.path.join(os.sep.join(get_yaml_config().get("app").get("image_resources_location")), image_uri)
    try:
        image = Image.open(full_image_path)
    except (FileNotFoundError) as e:
        logger.critical(f"{e}: Image does not exist! PATH: {full_image_path}")
        return Response(status_code=400, media_type='application/json', content=f"{e}")

    # Create a response with the appropriate content type
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    return Response(content=img_io.getvalue(), media_type='image/jpeg')


@router.post("/",
             response_class=HTMLResponse)
async def save_image(
            file: Annotated[bytes, File()],
            image_uri: Annotated[str, Form()]
            ):
    full_image_path = os.path.join(os.sep.join(get_yaml_config().get("app").get("image_resources_location")), image_uri)
    logger.info(f"Saving image. PATH: {full_image_path}")
    try:
        image = Image.open(io.BytesIO(file))
        image.save(full_image_path)
    except (Exception) as e:
        logger.critical(f"{e}: Error! PATH: {full_image_path}")
        return Response(status_code=400, media_type='text/html', content=f"{e}")
    logger.success(f"Image saved! PATH: {full_image_path}")
    return Response(status_code=200, media_type='text/html', content="Image saved!")


@router.delete("/",
               response_class=HTMLResponse)
async def delete_image(payload: schemas.ImageURI):
    full_image_path = os.path.join(os.sep.join(get_yaml_config().get("app").get("image_resources_location")), payload.image_uri)
    logger.info(f"Deleting image. PATH: {full_image_path}")
    try:
        os.remove(full_image_path)
    except (FileNotFoundError) as e:
        logger.critical(f"{e}: Image does not exist! PATH: {full_image_path}")
        return Response(status_code=400, media_type='text/html', content=f"{e}")
    logger.success(f"Image deleted! PATH: {full_image_path}")
    return Response(status_code=200, media_type='text/html', content="Image deleted!")
