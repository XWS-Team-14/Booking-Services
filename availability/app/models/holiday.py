from datetime import datetime
import uuid
from beanie import Document
from pydantic import Field


class Holiday(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    date: datetime
    title: str

    class Settings:
        indexes = [
            "id"
        ]
