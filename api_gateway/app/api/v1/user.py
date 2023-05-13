from typing import Annotated

import grpc
from fastapi import APIRouter, status, Cookie, Response
from fastapi_utils.cbv import cbv
from loguru import logger
from proto import user_pb2_grpc, user_pb2
from starlette.responses import Response

from app import schemas
from app.utils import get_server
from app.utils.jwt import get_id_from_access_token

router = APIRouter(
    tags=["User management"],
)


@cbv(router)
class User:
    @router.put(
        "/details",
        status_code=status.HTTP_200_OK,
        description="Update user details",
    )
    async def update_user_details(self, payload: schemas.UserDetailsUpdate,
                                  access_token: Annotated[str | None, Cookie()] = None) -> Response:
        user_id = get_id_from_access_token(access_token)
        logger.info(f"Tested update user details {user_id}")
        user_server = get_server("user_server")
        async with grpc.aio.insecure_channel(user_server) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            grpc_response = await stub.Update(user_pb2.User(
                id=str(user_id), first_name=payload.first_name, last_name=payload.last_name,
                home_address=payload.home_address, gender=payload.gender))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html",
                                content=grpc_response.error_message)
        return Response(
            status_code=200, media_type="text/html", content="User updated."
        )

    @router.delete(
        "/",
        status_code=status.HTTP_200_OK,
        description="Delete user",
    )
    async def delete(self, access_token: Annotated[str | None, Cookie()] = None) -> Response:
        user_id = get_id_from_access_token(access_token)
        logger.info(f"Tested delete user {user_id}")
        user_server = get_server("user_server")
        async with grpc.aio.insecure_channel(user_server) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            grpc_response = await stub.Delete(user_pb2.UserId(id=str(user_id)))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html",
                                content=grpc_response.error_message)
        return Response(
            status_code=200, media_type="text/html", content="User deleted."
        )
