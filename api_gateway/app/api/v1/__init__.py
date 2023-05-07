from fastapi import APIRouter

from app.api.v1 import auth
from app.config import get_yaml_config

config = get_yaml_config().get("app")
router = APIRouter(prefix=f"/{config.get('api_prefix')}")

# Include your endpoints here
router.include_router(auth.router, tags=["Authentication"])
