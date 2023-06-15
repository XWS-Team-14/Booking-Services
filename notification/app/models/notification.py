from pydantic import BaseModel

from app.models.accommodation import Accommodation
from app.models.notification_type import NotificationType
from app.models.receiver import Receiver
from app.models.sender import Sender


class Notification(BaseModel):
    type: NotificationType
    title: str
    content: str
    sender: Sender
    receiver: Receiver
    accommodation: Accommodation
    status: str
    timestamp: str
