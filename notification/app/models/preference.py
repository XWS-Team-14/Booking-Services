import uuid

from beanie import Document
from pydantic import BaseModel, Field

from app.models.notification_type import NotificationType
from app.models.receiver import Receiver


class Preference(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    type: NotificationType
    user: Receiver
    enabled: bool = True

    class Config:
        use_enum_values = True
