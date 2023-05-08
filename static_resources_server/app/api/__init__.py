from fastapi import APIRouter

from app.api import static

# include version of the api here
router = APIRouter(prefix="/api")
router.include_router(static.router)
