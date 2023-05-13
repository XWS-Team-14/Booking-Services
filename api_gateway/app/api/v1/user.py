from typing import Annotated

import grpc
from fastapi import APIRouter, status, Cookie, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger
from proto import credential_pb2_grpc, credential_pb2, user_pb2_grpc, user_pb2
from starlette.responses import Response

from app import schemas
from app.utils import get_server
from app.utils.jwt import get_id_from_token

router = APIRouter(
    tags=["User management"],
)


@cbv(router)
class User:
    @router.get("/active",
                status_code=status.HTTP_200_OK,
                description="Get currently active user", )
    async def get_active(self, access_token: Annotated[str | None, Cookie()] = None) -> Response:
        try:
            user_id = get_id_from_token(access_token)
        except ExpiredSignatureError:
            return Response(status_code=401, media_type="text/html", content="Token expired.")
        except InvalidTokenError:
            return Response(status_code=401, media_type="text/html", content="Invalid token.")
        logger.info(f"Tested delete user {user_id}")
        user_server = get_server("user_server")
        async with grpc.aio.insecure_channel(user_server) as channel:
            stub_user = user_pb2_grpc.UserServiceStub(channel)
            grpc_user_response = await stub_user.GetById(user_pb2.UserId(id=str(user_id)))
            if grpc_user_response.error_message:
                return Response(status_code=grpc_user_response.error_code, media_type="text/html",
                                content=grpc_user_response.error_message)
        user = {
            'first_name': grpc_user_response.first_name,
            'last_name': grpc_user_response.last_name,
            'gender': grpc_user_response.gender,
            'home_address': grpc_user_response.home_address
        }
        return JSONResponse(
            status_code=200, media_type="text/html", content=jsonable_encoder(user)
        )
    @router.put(
        "/details",
        status_code=status.HTTP_200_OK,
        description="Update user details",
    )
    async def update_user_details(self, payload: schemas.User,
                                  access_token: Annotated[str | None, Cookie()] = None) -> Response:
        try:
            user_id = get_id_from_token(access_token)
        except ExpiredSignatureError:
            return Response(status_code=401, media_type="text/html", content="Token expired.")
        except InvalidTokenError:
            return Response(status_code=401, media_type="text/html", content="Invalid token.")
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
        try:
            user_id = get_id_from_token(access_token)
        except ExpiredSignatureError:
            return Response(status_code=401, media_type="text/html", content="Token expired.")
        except InvalidTokenError:
            return Response(status_code=401, media_type="text/html", content="Invalid token.")
        logger.info(f"Tested delete user {user_id}")
        user_server = get_server("user_server")
        auth_server = get_server("auth_server")
        # TODO: Add accommodation and reservation checks.
        async with grpc.aio.insecure_channel(auth_server) as channel:
            stub_auth = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_auth_response = await stub_auth.Delete(credential_pb2.CredentialId(id=user_id))
            if grpc_auth_response.error_message:
                return Response(status_code=grpc_auth_response.error_code, media_type="text/html",
                                content=grpc_auth_response.error_message)
        async with grpc.aio.insecure_channel(user_server) as channel:
            stub_user = user_pb2_grpc.UserServiceStub(channel)
            grpc_user_response = await stub_user.Delete(user_pb2.UserId(id=str(user_id)))
            if grpc_user_response.error_message:
                return Response(status_code=grpc_user_response.error_code, media_type="text/html",
                                content=grpc_user_response.error_message)
        return Response(
            status_code=200, media_type="text/html", content="User deleted."
        )
