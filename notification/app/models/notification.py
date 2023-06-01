from app.models.receiver import Receiver
from app.models.sender import Sender


class Notification:
    key: str
    type: str
    title: str
    content: str
    sender: Sender
    receiver: Receiver
    status: str
    timestamp: str
