import datetime
import uuid

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from beanie import Document, Link, WriteRules, init_beanie

from app.models.accommodation import Accommodation
from app.models.host import Host


class Review(Document):
    id: UUID = Field(default_factory=uuid4)
    host: Link[Host]
    accommodation: Link[Accommodation]
    poster: str
    date: datetime
    host_rating: int
    accommodation_rating: int
