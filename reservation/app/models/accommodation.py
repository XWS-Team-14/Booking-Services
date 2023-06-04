import uuid

from beanie import Document


class Accommodation(Document):
    id: uuid.UUID
    automaticAccept: bool

    class Settings:
        indexes = [
            "id"
        ]
