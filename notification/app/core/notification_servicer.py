import json
import uuid

from firebase_admin import db
from google.protobuf.json_format import MessageToDict, MessageToJson
from loguru import logger

from app.models.notification_type import NotificationType
from app.models.preference import Preference
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
        notification = Notification(type=NotificationType[request.type], status=request.status,
                                    timestamp=request.timestamp, sender=sender, receiver=receiver,
                                    accommodation=accommodation, title='', content='')
        notification = generate(notification)
        message = json.loads(json.dumps(notification, default=lambda o: o.__dict__))
        ref.push(message)
        return notification_pb2.Empty()

    async def Initialize(self, request, context):
        """ Initializes user preferences.
            Input: User ID.
            Output: Empty, or error. """
        user = Receiver(id=request.id)
        if request.role == 'guest':
            preference_guest = Preference(type=NotificationType.GUEST_RESERVATION_UPDATE, user=user, enabled=True)
            await preference_guest.insert()
        else:
            for notification_type in NotificationType:
                if notification_type != NotificationType.GUEST_RESERVATION_UPDATE:
                    preference_host = Preference(type=notification_type, user=user, enabled=True)
                    await preference_host.insert()

        return notification_pb2.Empty()

    async def GetUserPreferences(self, request, context):
        """ Gets user preferences.
            Input: User ID.
            Output: Preference list. """
        logger.info(f'Fetching user {request.id} preferences')
        user_preferences = await Preference.find(Preference.user.id == request.id).to_list()
        user_preferences_dto = []
        for preference in user_preferences:
            dto = notification_pb2.Preference(id=str(preference.id), user_id=str(preference.user.id), type=preference.type,
                                              enabled=preference.enabled)
            user_preferences_dto.append(dto)
        return notification_pb2.UserPreferences(preference=user_preferences_dto)

    async def UpdateUserPreference(self, request, context):
        """ Updates a single user preference.
            Input: Preference.
            Output: Empty, or error. """
        logger.info(f'Updating user {request.user_id} preference {request.type} to {request.enabled}')
        preference = await Preference.get(request.id)
        preference.enabled = request.enabled
        await preference.save()

        return notification_pb2.Empty()
