from beanie import Document
from pydantic import UUID4
from pydantic import Field
import uuid
from datetime import datetime

from app.models.accommodation import Accommodation
class DeletedAccommodation(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    item: Accommodation
    transaction_id: uuid.UUID
    timestamp: datetime
    