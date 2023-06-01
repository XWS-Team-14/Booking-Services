from loguru import logger
from proto import notification_pb2, notification_pb2_grpc

from firebase_admin import db

from google.protobuf.json_format import MessageToJson, MessageToDict


class NotificationServicer(notification_pb2_grpc.NotificationServiceServicer):
    async def Send(self, request, context):
        """ Saves notification to Firebase Realtime Database.
            Input: Notification.
            Output: Empty, or error. """
        logger.info('Request received')
        ref = db.reference(f'notifications/{request.receiver.id}')
        notification = MessageToDict(request)
        ref.push(notification)
        return notification_pb2.Empty()
