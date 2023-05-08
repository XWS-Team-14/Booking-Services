import io
import os
from fastapi.responses import Response
from PIL import Image
from fastapi import APIRouter, status
from fastapi_utils.cbv import cbv
from loguru import logger
from app.config import get_yaml_config
from app import schemas

router = APIRouter()


@router.get("/images/{image_uri}")
async def get_image(image_uri: str):
    # Retrive image using PIL
    full_image_path = os.path.join(get_yaml_config().get("app").get("image_resources_location"), image_uri)
    image = Image.open(full_image_path)

    # Create a response with the appropriate content type
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    return Response(content=img_io.getvalue(), media_type='image/jpeg')


@router.post("/images")
async def save_image(self, payload: schemas.ImagePost):
    full_image_path = os.path.join(get_yaml_config().get("app").get("image_resources_location"), payload.image_uri)
    logger.info(f"Saving image. PATH: {full_image_path}")
    try:
        image = Image.open(io.BytesIO(payload.data))
        image.save(full_image_path)
    except (Exception) as e:
        logger.critical(f"{e}: Error! PATH: {full_image_path}")
        return Response(status_code=400, media_type='application/json', content="{}")
    logger.success(f"Image saved! PATH: {full_image_path}")
    return Response(status_code=200, media_type='application/json', content="{}")


@router.delete("/images")
async def delete_image(self, payload: schemas.ImageDelete):
    full_image_path = os.path.join(get_yaml_config().get("app").get("image_resources_location"), payload.image_uri)
    logger.info(f"Deleting image. PATH: {full_image_path}")
    try:
        os.remove(full_image_path)
    except (FileNotFoundError) as e:
        logger.critical(f"{e}: Image does not exist! PATH: {full_image_path}")
        return Response(status_code=400, media_type='application/json', content="{}")
    logger.success(f"Image deleted! PATH: {full_image_path}")
    return Response(status_code=200, media_type='application/json', content="{}")
