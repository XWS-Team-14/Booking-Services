from fastapi import APIRouter, status
from fastapi_utils.cbv import cbv
from loguru import logger

from app import schema

router = APIRouter()


@cbv(router)
class Accommodation:
    # Useful for shared dependencies
    @router.delete(
        "/test",
        status_code=status.HTTP_204_NO_CONTENT,
        description="Test fastapi",
    )
    async def test(self, payload: schemas.AccommodationDelete) -> None:
        logger.info(f"App tested and got number {payload.id}")


@router.delete(
    "/test2",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Test fastapi",
)
async def test(self, payload: schemas.AccommodationDelete) -> None:
    logger.info(f"App tested and got number {payload.id}")
