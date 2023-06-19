from uuid import UUID, uuid4

from beanie import Document, Link
from pydantic import Field

from app.models.host import Host


class Accommodation(Document):
    id: UUID = Field(default_factory=uuid4)
    host: Link[Host]
    review_count: int = 0
    rating_sum: int = 0

    def get_average_rating(self):
        return self.rating_sum / self.review_count if self.review_count else 0
