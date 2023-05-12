from fastapi import APIRouter

from .auth import router as auth_router
from .accommodation import router as accommodation_router
from .user import router as user_router

# include version of the api here
router = APIRouter(prefix="/api")
router.include_router(auth_router, prefix="/auth")
router.include_router(accommodation_router, prefix="/accommodation")
router.include_router(user_router, prefix="/user")