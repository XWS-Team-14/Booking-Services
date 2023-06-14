from beanie import Document
from pydantic import UUID4
import uuid
from datetime import datetime

from app.models.accommodation import Accommodation
class DeletedAccommodation(Document):
    id: UUID4
    item: Accommodation
    transaction_id: uuid.UUID
    timestamp: datetime
    