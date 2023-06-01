import uuid

from app.models.notification_status import NotificationStatus
from app.models.notification_type import NotificationType
from app.models.receiver import Receiver
from app.models.sender import Sender


class Notification:
    key: str
    type: NotificationType
    title: str
    content: str
    sender: Sender
    receiver: Receiver
    status: NotificationStatus
    timestamp: str
