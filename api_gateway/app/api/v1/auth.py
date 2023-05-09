from fastapi import APIRouter, status
from fastapi_utils.cbv import cbv
from loguru import logger

from app import schemas

router = APIRouter(
    tags=["Auth"],
)


@cbv(router)
class Auth:
    @router.post(
        "/register",
        status_code=status.HTTP_200_OK,
        description="Register user",
    )
    async def register(self, payload: schemas.Register) -> None:
        logger.info(f"Tested register {payload.email}")

    @router.post(
        "/login",
        status_code=status.HTTP_200_OK,
        description="Log in user",
    )
    async def login(self, payload: schemas.Login) -> None:
        logger.info(f"Tested login {payload.email}")
