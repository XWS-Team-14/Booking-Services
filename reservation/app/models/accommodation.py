import uuid

from beanie import Document
from pydantic import Field


class Accommodation(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    automaticAccept: bool

    class Settings:
        indexes = [
            "id"
        ]
