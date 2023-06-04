import uuid

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from beanie import Document, Link, WriteRules, init_beanie
class Guest(Document):
    id: UUID = Field(default_factory=uuid4)
    canceledReservations: int = 0

    class Settings:
        indexes = [
            "id"
        ]
