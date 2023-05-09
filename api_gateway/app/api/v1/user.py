from fastapi import APIRouter, status
from fastapi_utils.cbv import cbv
from loguru import logger

from app import schemas

router = APIRouter(
    tags=["User management"],
)


@cbv(router)
class User:
    @router.put(
        "/details/{user_id}",
        status_code=status.HTTP_200_OK,
        description="Update user details",
    )
    async def update_user_details(self, user_id, payload: schemas.UserDetailsUpdate) -> None:
        logger.info(f"Tested register {user_id}")

    @router.delete(
        "/{user_id}",
        status_code=status.HTTP_200_OK,
        description="Delete user",
    )
    async def login(self, payload: schemas.Login) -> None:
        logger.info(f"Tested login {payload.email}")