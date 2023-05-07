import uuid
from beanie import Document

from app.models.gender import Gender


class User(Document):
    id: uuid.UUID
    first_name: str
    last_name: str
    home_address: str
    gender: Gender