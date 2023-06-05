import uuid

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from beanie import Document, Link, WriteRules, init_beanie


class Host(Document):
    id: UUID = Field(default_factory=uuid4)
    review_count: int = 0
    rating_sum: int = 0
    cancellation_rate: float = 0.0
    reservation_days: int = 0
    reservation_count: int = 0
