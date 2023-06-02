from pydantic import BaseModel

from app.models.accommodation import Accommodation
from app.models.receiver import Receiver
from app.models.sender import Sender


class Notification(BaseModel):
    type: str
    title: str
    content: str
    sender: Sender
    receiver: Receiver
    accommodation: Accommodation
    status: str
    timestamp: str
