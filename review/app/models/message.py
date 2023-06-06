from datetime import datetime
import uuid

from beanie import Document
from pydantic import Field

from app.models.message_status import MessageStatus


class Message(Document):
    id: uuid.UUID
    timestamp: datetime
    status: MessageStatus
