import uuid

from fastapi import APIRouter, status, Cookie
from fastapi.responses import HTMLResponse, Response
from fastapi_utils.cbv import cbv
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger
import grpc
from starlette.responses import Response
from typing import Annotated

from app.constants import auth_server, user_server, reservation_server
from app.utils.jwt import get_id_from_token

from fastapi.responses import JSONResponse
from app import schemas
from app.config import get_yaml_config
from proto import credential_pb2_grpc, credential_pb2, user_pb2_grpc, user_pb2, reservation_crud_pb2, \
    reservation_crud_pb2_grpc

from app.utils import get_server
from opentelemetry.instrumentation.grpc import aio_client_interceptors

router = APIRouter()


@cbv(router)
class Auth:
    @router.post(
        "/register", response_class=HTMLResponse,
        description="Register user",
    )
    async def register(self, payload: schemas.Register) -> Response:
        logger.info(f"Tested register {payload.email}")
        user_id = uuid.uuid4()
        async with grpc.aio.insecure_channel(auth_server, interceptors=aio_client_interceptors()) as channel:
            stub = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_response = await stub.Register(credential_pb2.Credential(
                id=str(user_id), email=payload.email, password=payload.password, role=payload.role, active=True))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html",
                                content=grpc_response.error_message)

        async with grpc.aio.insecure_channel(user_server, interceptors=aio_client_interceptors()) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            await stub.Register(user_pb2.User(
                id=str(user_id), first_name=payload.first_name, last_name=payload.last_name,
                home_address=payload.home_address, gender=payload.gender))
        if payload.role == "guest":
            async with grpc.aio.insecure_channel(reservation_server, interceptors=aio_client_interceptors()) as channel:
                stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
                await stub.CreateGuest(reservation_crud_pb2.Guest(
                    id=str(user_id), canceledReservations=0))
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
        async with grpc.aio.insecure_channel(auth_server, interceptors=aio_client_interceptors()) as channel:
            stub = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_response = await stub.Login(credential_pb2.Credential(email=payload.email, password=payload.password))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html",
                                content=grpc_response.error_message)
            access_token = grpc_response.access_token
            refresh_token = grpc_response.refresh_token
        response = Response(
            status_code=200, media_type="text/html", content=f"{access_token}"
        )
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        return response

    @router.post(
        "/logout",
        status_code=status.HTTP_200_OK,
        description="Log out user",
    )
    async def logout(self, access_token: Annotated[str | None, Cookie()] = None) -> Response:
        logger.info(f"Tested logout {access_token}")
        try:
            user_id = get_id_from_token(access_token)
        except ExpiredSignatureError:
            return Response(status_code=401, media_type="text/html", content="Token expired.")
        except InvalidTokenError:
            return Response(status_code=401, media_type="text/html", content="Invalid token.")
        response = Response(
            status_code=200, media_type="text/html", content=f"Logged out"
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

    @router.post(
        "/token/refresh",
        status_code=status.HTTP_200_OK,
        description="Refresh access token",
    )
    async def refresh_token(self, refresh_token: Annotated[str | None, Cookie()] = None) -> Response:
        user_id = get_id_from_token(refresh_token, "refresh")
        logger.info(f"Tested refresh token for user {user_id}")
        async with grpc.aio.insecure_channel(auth_server, interceptors=aio_client_interceptors()) as channel:
            stub = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_response = await stub.RefreshToken(credential_pb2.TokenRefresh(
                refresh_token=refresh_token))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html",
                                content=grpc_response.error_message)
            access_token = grpc_response.access_token
            refresh_token = grpc_response.refresh_token
        response = Response(
            status_code=200, media_type="text/html", content=f"Access: {access_token}\n Refresh: {refresh_token}"
        )
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        return response

    @router.put(
        "/password",
        status_code=status.HTTP_200_OK,
        description="Update user's password",
    )
    async def update_password(self, payload: schemas.PasswordUpdate,
                              access_token: Annotated[str | None, Cookie()] = None) -> Response:
        logger.info(f"Tested password update {access_token}")
        try:
            user_id = get_id_from_token(access_token)
        except ExpiredSignatureError:
            return Response(status_code=401, media_type="text/html", content="Token expired.")
        except InvalidTokenError:
            return Response(status_code=401, media_type="text/html", content="Invalid token.")
        async with grpc.aio.insecure_channel(auth_server, interceptors=aio_client_interceptors()) as channel:
            stub = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_response = await stub.UpdatePassword(credential_pb2.PasswordUpdate(
                id=user_id, old_password=payload.old_password,
                new_password=payload.new_password))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html",
                                content=grpc_response.error_message)
        return Response(
            status_code=200, media_type="text/html", content=f"Password changed.")

    @router.put(
        "/email",
        status_code=status.HTTP_200_OK,
        description="Update user's email",
    )
    async def update_email(self, payload: schemas.EmailUpdate,
                           access_token: Annotated[str | None, Cookie()] = None) -> Response:
        logger.info(f"Tested email update {access_token}")
        try:
            user_id = get_id_from_token(access_token)
        except ExpiredSignatureError:
            return Response(status_code=401, media_type="text/html", content="Token expired.")
        except InvalidTokenError:
            return Response(status_code=401, media_type="text/html", content="Invalid token.")
        async with grpc.aio.insecure_channel(auth_server, interceptors=aio_client_interceptors()) as channel:
            stub = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_response = await stub.UpdateEmail(credential_pb2.EmailUpdate(
                id=user_id, old_email=payload.old_email,
                new_email=payload.new_email))
            if grpc_response.error_message:
                return Response(status_code=grpc_response.error_code, media_type="text/html",
                                content=grpc_response.error_message)
        return Response(
            status_code=200, media_type="text/html", content=f"Email changed.")
