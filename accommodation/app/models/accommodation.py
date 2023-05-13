from beanie import Document
from pydantic import UUID4

from .location import Location


class Accommodation(Document):
    id: UUID4
    user_id: UUID4
    name: str
    location: Location
    features: list[str]
    image_urls: list[str]
    min_guests: int
    max_guests: int

    class Settings:
        indexes = [
            "id",
        ]
