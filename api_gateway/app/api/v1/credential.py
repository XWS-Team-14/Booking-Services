from fastapi import APIRouter, status
from fastapi_utils.cbv import cbv
from loguru import logger

from app import schemas

router = APIRouter(
    tags=["Credential management"],
)


@cbv(router)
class User:
    @router.put(
        "/email/{user_id}",
        status_code=status.HTTP_200_OK,
        description="Update user's email",
    )
    async def update_email(self, user_id, payload: schemas.PasswordUpdate) -> None:
        logger.info(f"Tested email update {user_id}")

    @router.put(
        "/password/{user_id}",
        status_code=status.HTTP_200_OK,
        description="Update user's password",
    )
    async def update_password(self, user_id, payload: schemas.PasswordUpdate) -> None:
        logger.info(f"Tested password update {user_id}")
