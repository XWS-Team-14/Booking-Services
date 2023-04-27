import uuid
from pydantic import BaseModel


class AccommodationDelete(BaseModel):
    id: uuid.UUID
