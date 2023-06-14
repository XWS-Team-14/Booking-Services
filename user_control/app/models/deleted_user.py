import uuid
from beanie import Document
from pydantic import Field
from datetime import datetime

from app.models.user import User

class DeletedUser(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    item: User
    transaction_id: uuid.UUID
    timestamp: datetime
    