import uuid

from beanie import Document
from pydantic import BaseModel


class Guest (Document):
    id : uuid.UUID
    canceledReservations : int

    class Settings:
        indexes = [
            "id"
        ]