from fastapi import APIRouter

from . import auth
from . import accommodation
from app.config import get_yaml_config
from .availability import router as availability_router

config = get_yaml_config().get("app")
router = APIRouter(prefix=f"/{config.get('api_prefix')}")

# Include your endpoints here
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(
    accommodation.router, prefix="/accommodation", tags=["Accommodation"]
)
router.include_router(availability_router, prefix="/avail")
