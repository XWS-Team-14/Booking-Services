import httpx
from fastapi import APIRouter
from fastapi.responses import FileResponse, Response
from loguru import logger
from app.config import get_yaml_config

router = APIRouter()


@router.get(
    "/{image_uri}",
    description="Get image from static server",
    response_class=FileResponse,
    status_code=200,
)
async def get_image(image_uri: str):
    """Sends request to static image server for an image

    Pases image back to requester. Editable server config in config.yaml
    """
    logger.info("Getting image from static resource server! Image uri: " + image_uri)
    image = httpx.get(get_yaml_config().get("static_server").get("url") + image_uri)
    return Response(content=image.content, media_type="image/jpeg")
