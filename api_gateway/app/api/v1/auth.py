import uuid

from fastapi import APIRouter, status, Cookie
from fastapi.responses import HTMLResponse, Response
from fastapi_utils.cbv import cbv
from loguru import logger
import grpc
from starlette.responses import Response
from typing import Annotated
from app.utils.jwt import get_id_from_access_token

from app import schemas
from app.config import get_yaml_config
from proto import credential_pb2_grpc, credential_pb2, user_pb2_grpc, user_pb2

from app.utils import get_server

router = APIRouter(
    tags=["Auth"],
)


@cbv(router)
class Auth:
    @router.post(
        "/register", response_class=HTMLResponse,
        description="Register user",
    )
    async def register(self, payload: schemas.Register) -> Response:
        logger.info(f"Tested register {payload.email}")
        auth_server = get_server("auth_server")
        user_server = get_server("user_server")
        user_id = uuid.uuid4()
        async with grpc.aio.insecure_channel(auth_server) as channel:
            stub = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_response = await stub.Register(credential_pb2.Credential(
                id=str(user_id), email=payload.email, password=payload.password, role=payload.role, active=True))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html", content=grpc_response.error_message)

        async with grpc.aio.insecure_channel(user_server) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            await stub.Register(user_pb2.User(
                id=str(user_id), first_name=payload.first_name, last_name=payload.last_name,
                home_address=payload.home_address, gender=payload.gender))
        return Response(
            status_code=200, media_type="text/html", content="User registered."
        )

    @router.post(
        "/login",
        status_code=status.HTTP_200_OK,
        description="Log in user",
    )
    async def login(self, payload: schemas.Login) -> Response:
        logger.info(f"Tested login {payload.email}")
        auth_server = get_server("auth_server")
        async with grpc.aio.insecure_channel(auth_server) as channel:
            stub = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_response = await stub.Login(credential_pb2.Credential(
               email=payload.email, password=payload.password))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html", content=grpc_response.error_message)
            access_token = grpc_response.access_token
            refresh_token = grpc_response.refresh_token
        response = Response(
            status_code=200, media_type="text/html", content=f"User logged in."
        )
        print(access_token)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        return response

    @router.put(
        "/password",
        status_code=status.HTTP_200_OK,
        description="Update user's password",
    )
    async def update_password(self,  payload: schemas.PasswordUpdate, access_token: Annotated[str | None, Cookie()] = None) -> Response:
        logger.info(f"Tested password update {access_token}")
        auth_server = get_server("auth_server")
        async with grpc.aio.insecure_channel(auth_server) as channel:
            stub = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_response = await stub.UpdatePassword(credential_pb2.PasswordUpdate(
                id=get_id_from_access_token(access_token), old_password = payload.old_password, new_password = payload.new_password))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html",
                                content=grpc_response.error_message)
        return Response(
            status_code=200, media_type="text/html", content=f"Password changed.")