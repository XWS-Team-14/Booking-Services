from fastapi import APIRouter, status
from fastapi_utils.cbv import cbv
from loguru import logger

from app import schema
from app.schema.auth import Register, Login

router = APIRouter()


@router.post(
    "/auth/register",
    status_code=status.HTTP_200_OK,
    description="Register user",
)
async def register(details: Register) -> None:
    logger.info(f"Register HTTP request received")

@router.post(
    "/auth/login",
    status_code=status.HTTP_200_OK,
    description="Login user",
)
async def login(details: Login) -> None:
    logger.info(f"Login HTTP request received")