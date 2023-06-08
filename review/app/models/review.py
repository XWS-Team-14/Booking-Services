from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Link
from pydantic import Field

from app.models.accommodation import Accommodation
from app.models.host import Host


class Review(Document):
    id: UUID = Field(default_factory=uuid4)
    host: Link[Host]
    accommodation: Link[Accommodation]
    poster: str
    timestamp: datetime
    host_rating: int
    accommodation_rating: int
