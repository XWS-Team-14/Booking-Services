
from pydantic import UUID4, BaseModel


class Location(BaseModel):
    id: UUID4
    country: str
    city: str
    address: str
