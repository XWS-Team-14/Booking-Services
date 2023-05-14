from fastapi import APIRouter

from ..api import v1
from . import static

# include version of the api here
router = APIRouter(prefix="/api")
router.include_router(v1.router)
router.include_router(static.router)
