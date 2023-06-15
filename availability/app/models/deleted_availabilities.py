from datetime import datetime
from app.models.availability import Availability
import uuid
from pydantic import Field
from beanie import Document

class DeletedAvailability(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    item: Availability
    transaction_id: uuid.UUID
    timestamp: datetime
    