import json

from firebase_admin import db
from google.protobuf.json_format import MessageToDict, MessageToJson
from loguru import logger
from proto import notification_pb2, notification_pb2_grpc

from app.core.notification_helper import generate
from app.models.accommodation import Accommodation

from app.models.notification import Notification
from app.models.receiver import Receiver
from app.models.sender import Sender


class NotificationServicer(notification_pb2_grpc.NotificationServiceServicer):
    async def Send(self, request, context):
        """ Saves notification to Firebase Realtime Database.
            Input: Notification.
            Output: Empty, or error. """
        logger.info('Request received')
        ref = db.reference(f'notifications/{request.receiver.id}')
        sender = Sender(id=request.sender.id, name=request.sender.name)
        receiver = Receiver(id=request.receiver.id)
        accommodation = Accommodation(id=request.accommodation.id, name=request.accommodation.name)
        notification = Notification(type=request.type, status=request.status, timestamp=request.timestamp, sender=sender, receiver=receiver, accommodation=accommodation, title='', content='')
        notification = generate(notification)
        message = json.loads(json.dumps(notification, default=lambda o: o.__dict__))
        ref.push(message)
        return notification_pb2.Empty()
