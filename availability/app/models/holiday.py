from datetime import datetime
import uuid
from beanie import Document


class Holiday(Document):
    holiday_id: uuid.UUID
    date: datetime
    title: str

    class Settings:
        indexes = [
            "holiday_id"
        ]
