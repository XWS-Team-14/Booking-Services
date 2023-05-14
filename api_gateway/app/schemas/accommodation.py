import uuid
from pydantic import BaseModel


class AccommodationDelete(BaseModel):
    id: uuid.UUID

class Location(BaseModel):
    country: str
    city: str
    address: str