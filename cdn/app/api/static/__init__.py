from fastapi import APIRouter

from app.api.static.endpoints import image
from app.config import get_yaml_config

config = get_yaml_config().get("app")
router = APIRouter(prefix=f"/{config.get('api_prefix')}")

# Include your endpoints here
router.include_router(image.router, prefix="/images", tags=["Images"])
