from fastapi import APIRouter

from .auth import router as auth_router
from .accommodation import router as accommodation_router
from .user import router as user_router
from .availability import router as availability_router
from .reservation import router as reservation_router
from ...config import get_yaml_config

config = get_yaml_config().get("app")
router = APIRouter(prefix=f"/{config.get('api_prefix')}")
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(accommodation_router, prefix="/accommodation", tags=["Accommodation"])
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(availability_router, prefix="/avail", tags=["Availability"])
router.include_router(reservation_router, prefix="/reservation")
router.include_router(accommodation_router, prefix="/accommodation")

