import asyncio
import datetime
import json
from typing import Annotated

import grpc
from fastapi import APIRouter, status, Cookie, Response
from fastapi.encoders import jsonable_encoder
from fastapi import WebSocket
from websockets.exceptions import ConnectionClosedError
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from google.protobuf import json_format
from kafka import KafkaProducer
from kafka.errors import KafkaError
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger
from proto import (
    credential_pb2_grpc,
    credential_pb2,
    user_pb2_grpc,
    user_pb2,
    accommodation_pb2_grpc,
    accommodation_pb2,
    reservation_crud_pb2_grpc,
    reservation_crud_pb2,
)
from starlette.responses import Response

from app import schemas
from app.constants import user_server, reservation_server, auth_server, accommodation_server, kafka_server
from app.utils import get_server
from app.utils.jwt import get_id_from_token, get_role_from_token

router = APIRouter()


@cbv(router)
class User:
    @router.websocket("/status")
    async def websocket_endpoint(self, websocket: WebSocket):


        await websocket.accept()
        while True:

            t = datetime.datetime.utcnow().time()
            try:
                #await websocket.send_text(str(t))
                await asyncio.sleep(1)
            except ConnectionClosedError:
                print("Client disconnected.")
                break
    @router.get(
        "/active",
        response_class=JSONResponse,
        status_code=status.HTTP_200_OK,
        description="Get currently active user",
    )
    async def get_active(
        self, access_token: Annotated[str | None, Cookie()] = None
    ) -> Response:
        try:
            user_id = get_id_from_token(access_token)
        except ExpiredSignatureError:
            return Response(
                status_code=401, media_type="text/html", content="Token expired."
            )
        except InvalidTokenError:
            return Response(
                status_code=401, media_type="text/html", content="Invalid token."
            )
        logger.info(f"Tested delete user {user_id}")
        async with grpc.aio.insecure_channel(user_server) as channel:
            stub_user = user_pb2_grpc.UserServiceStub(channel)
            grpc_user_response = await stub_user.GetById(
                user_pb2.UserId(id=str(user_id))
            )
            if grpc_user_response.error_message:
                return Response(
                    status_code=grpc_user_response.error_code,
                    media_type="text/html",
                    content=grpc_user_response.error_message,
                )
        user = {
            'id': user_id,
            'first_name': grpc_user_response.first_name,
            'last_name': grpc_user_response.last_name,
            'gender': grpc_user_response.gender,
            'home_address': grpc_user_response.home_address
        }
        return JSONResponse(
            status_code=200, media_type="text/html", content=jsonable_encoder(user)
        )

    @router.get(
        "/{user_id}",
        status_code=status.HTTP_200_OK,
        description="Get user by id",
    )
    async def get_by_id(self, user_id) -> Response:
        logger.info(f"Tested get user by id {user_id}")
        async with grpc.aio.insecure_channel(user_server) as channel:
            stub_user = user_pb2_grpc.UserServiceStub(channel)
            grpc_user_response = await stub_user.GetById(
                user_pb2.UserId(id=str(user_id))
            )
            if grpc_user_response.error_message:
                return Response(
                    status_code=grpc_user_response.error_code,
                    media_type="text/html",
                    content=grpc_user_response.error_message,
                )
        user = {
            "first_name": grpc_user_response.first_name,
            "last_name": grpc_user_response.last_name,
            "gender": grpc_user_response.gender,
            "home_address": grpc_user_response.home_address,
        }
        return JSONResponse(
            status_code=200, media_type="text/html", content=jsonable_encoder(user)
        )

    @router.put(
        "/details",
        status_code=status.HTTP_200_OK,
        description="Update user details",
    )
    async def update_user_details(
        self,
        payload: schemas.User,
        access_token: Annotated[str | None, Cookie()] = None,
    ) -> Response:
        try:
            user_id = get_id_from_token(access_token)
        except ExpiredSignatureError:
            return Response(
                status_code=401, media_type="text/html", content="Token expired."
            )
        except InvalidTokenError:
            return Response(
                status_code=401, media_type="text/html", content="Invalid token."
            )
        logger.info(f"Tested update user details {user_id}")
        async with grpc.aio.insecure_channel(user_server) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            grpc_response = await stub.Update(
                user_pb2.User(
                    id=str(user_id),
                    first_name=payload.first_name,
                    last_name=payload.last_name,
                    home_address=payload.home_address,
                    gender=payload.gender,
                )
            )
            if grpc_response.error_message:
                return Response(
                    status_code=grpc_response.error_code,
                    media_type="text/html",
                    content=grpc_response.error_message,
                )
        return Response(
            status_code=200, media_type="text/html", content="User updated."
        )

    @router.delete(
        "/",
        status_code=status.HTTP_200_OK,
        description="Delete user",
    )
    async def delete(
        self, access_token: Annotated[str | None, Cookie()] = None
    ) -> Response:
        try:
            user_id = get_id_from_token(access_token)
            user_role = get_role_from_token(access_token)
        except ExpiredSignatureError:
            return Response(
                status_code=401, media_type="text/html", content="Token expired."
            )
        except InvalidTokenError:
            return Response(
                status_code=401, media_type="text/html", content="Invalid token."
            )
        logger.info(f"Tested delete user {user_id}")

        if user_role == "host":
            async with grpc.aio.insecure_channel(reservation_server) as channel:
                stub_reservation = reservation_crud_pb2_grpc.ReservationCrudStub(
                    channel
                )
                data = await stub_reservation.GetActiveByHost(
                    reservation_crud_pb2.HostId(id=user_id)
                )
                if (
                    len(
                        json_format.MessageToDict(
                            data, preserving_proto_field_name=True
                        )
                    )
                    > 0
                ):
                    return Response(
                        status_code=403,
                        media_type="text/html",
                        content="User has active reservations.",
                    )
        else:
            async with grpc.aio.insecure_channel(reservation_server) as channel:
                stub_reservation = reservation_crud_pb2_grpc.ReservationCrudStub(
                    channel
                )
                data = await stub_reservation.GetActiveByGuest(
                    reservation_crud_pb2.GuestId(guest_id=user_id)
                )
                if (
                    len(
                        json_format.MessageToDict(
                            data, preserving_proto_field_name=True
                        )
                    )
                    > 0
                ):
                    return Response(
                        status_code=403,
                        media_type="text/html",
                        content="User has active reservations.",
                    )

        async with grpc.aio.insecure_channel(auth_server) as channel:
            stub_auth = credential_pb2_grpc.CredentialServiceStub(channel)
            grpc_auth_response = await stub_auth.Delete(
                credential_pb2.CredentialId(id=user_id)
            )
            if grpc_auth_response.error_message:
                return Response(
                    status_code=grpc_auth_response.error_code,
                    media_type="text/html",
                    content=grpc_auth_response.error_message,
                )

        async with grpc.aio.insecure_channel(user_server) as channel:
            stub_user = user_pb2_grpc.UserServiceStub(channel)
            grpc_user_response = await stub_user.Delete(
                user_pb2.UserId(id=str(user_id))
            )
            if grpc_user_response.error_message:
                return Response(
                    status_code=grpc_user_response.error_code,
                    media_type="text/html",
                    content=grpc_user_response.error_message,
                )

        if user_role == "host":
            async with grpc.aio.insecure_channel(accommodation_server) as channel:
                stub_accommodation = accommodation_pb2_grpc.AccommodationServiceStub(
                    channel
                )
                await stub_accommodation.DeleteByUser(
                    accommodation_pb2.InputId(id=user_id)
                )
        response = Response(
            status_code=200, media_type="text/html", content="User deleted."
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
