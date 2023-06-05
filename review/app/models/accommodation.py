import uuid

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from beanie import Document, Link, WriteRules, init_beanie

from app.models.host import Host


class Accommodation(Document):
    id: UUID = Field(default_factory=uuid4)
    host: Link[Host]
    review_count: int = 0
    rating_sum: int = 0
