
from typing import Annotated

import grpc
from fastapi import APIRouter, Cookie
from fastapi_utils.cbv import cbv
from google.protobuf.json_format import MessageToJson

from app.utils.jwt import get_role_from_token, get_id_from_token
from proto import notification_pb2_grpc, notification_pb2
from starlette.responses import HTMLResponse, Response

from app import schemas
from app.constants import notification_server
from app.utils import get_server
from opentelemetry.instrumentation.grpc import aio_client_interceptors
from jwt import ExpiredSignatureError, InvalidTokenError

router = APIRouter()


@cbv(router)
class Notification:
    @router.post(
        "/", response_class=HTMLResponse,
        description="Send a notification",
    )
    async def send(self, payload: schemas.Notification) -> Response:
        sender = notification_pb2.Sender(id=payload.sender.id, name=payload.sender.name)
        receiver = notification_pb2.Receiver(id=payload.receiver.id)
        accommodation = notification_pb2.Accommodation(id=payload.accommodation.id, name=payload.accommodation.name)
        notification = notification_pb2.Notification(type=payload.type,
                                                     sender=sender, receiver=receiver, status=payload.status,
                                                     accommodation=accommodation,
                                                     timestamp=payload.timestamp)
        async with grpc.aio.insecure_channel(notification_server, interceptors=aio_client_interceptors()) as channel:
            stub = notification_pb2_grpc.NotificationServiceStub(channel)
            await stub.Send(notification)
        return Response(
            status_code=200, media_type="text/html", content="Notification sent."
        )

    @router.get("/preference", description="Get user preferences")
    async def get_user_preferences(self, access_token: Annotated[str | None, Cookie()] = None) -> Response:
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
        async with grpc.aio.insecure_channel(notification_server, interceptors=aio_client_interceptors()) as channel:
            stub = notification_pb2_grpc.NotificationServiceStub(channel)
            preferences = await stub.GetUserPreferences(notification_pb2.Receiver(id=user_id, role=user_role))
        return Response(
            status_code=200, media_type="application/json", content=MessageToJson(preferences)
        )

    @router.put("/preference/{id}", description="Update user preference")
    async def update_user_preference(self, id, payload: schemas.Preference, access_token: Annotated[str | None, Cookie()] = None):
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
        if str(user_id) != payload.user_id:
            return Response(status_code=401, media_type="text/html", content="Unauthorized.")
        async with grpc.aio.insecure_channel(notification_server, interceptors=aio_client_interceptors()) as channel:
            stub = notification_pb2_grpc.NotificationServiceStub(channel)
            await stub.UpdateUserPreference(notification_pb2.Preference(id=id, user_id=user_id, enabled=payload.enabled, type=payload.type))
        return Response(
            status_code=200, media_type="text/html", content='Updated.'
        )
