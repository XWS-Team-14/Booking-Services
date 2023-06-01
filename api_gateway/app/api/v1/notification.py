import json

import grpc
from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from google.protobuf.json_format import Parse, ParseDict
from proto import notification_pb2_grpc, notification_pb2
from starlette.responses import HTMLResponse, Response

from app import schemas
from app.utils import get_server

router = APIRouter()


@cbv(router)
class Notification:
    @router.post(
        "/", response_class=HTMLResponse,
        description="Send a notification",
    )
    async def send(self, payload: schemas.Notification) -> Response:
        notification_server = get_server("notification_server")
        sender = notification_pb2.Sender(id=payload.sender.id, name=payload.sender.name)
        receiver = notification_pb2.Receiver(id=payload.receiver.id)
        notification = notification_pb2.Notification(type=payload.type, title=payload.title, content=payload.content,
                                                     sender=sender, receiver=receiver, status=payload.status,
                                                     timestamp=payload.timestamp)
        async with grpc.aio.insecure_channel(notification_server) as channel:
            stub = notification_pb2_grpc.NotificationServiceStub(channel)
            await stub.Send(notification)
        return Response(
            status_code=200, media_type="text/html", content="Notification sent."
        )
