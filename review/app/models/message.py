import uuid
from datetime import datetime

from beanie import Document

from app.models.message_status import MessageStatus


class Message(Document):
    id: uuid.UUID
    timestamp: datetime
    status: MessageStatus
