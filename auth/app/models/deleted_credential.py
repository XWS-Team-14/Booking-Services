from datetime import datetime
from app.models.credential import Credential
import uuid
from pydantic import Field
from beanie import Document

class DeletedCredential(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    item: Credential
    transaction_id: uuid.UUID
    timestamp: datetime
    