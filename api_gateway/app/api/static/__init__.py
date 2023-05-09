from fastapi import APIRouter

from app.config import get_yaml_config
from app.api.static.endpoints import images

config = get_yaml_config().get("app")
router = APIRouter(prefix=f"/{config.get('static_prefix')}")

# Include your endpoints here
router.include_router(images.router, prefix="/images", tags=["Images"])
