import grpc
from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from proto import notification_pb2_grpc, notification_pb2
from starlette.responses import HTMLResponse, Response

from app import schemas
from app.constants import notification_server
from app.utils import get_server
from opentelemetry.instrumentation.grpc import aio_client_interceptors

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
