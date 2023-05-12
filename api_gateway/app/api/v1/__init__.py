from fastapi import APIRouter

from .auth import router as auth_router
from .accommodation import router as accommodation_router
from .availability import router as availability_router

# include version of the api here
router = APIRouter(prefix="/api")
router.include_router(auth_router, prefix="/auth")
router.include_router(accommodation_router, prefix="/accommodation")
router.include_router(availability_router, prefix="/avail")