from pydantic import BaseModel


class Location(BaseModel):
    country: str = ""
    city: str = ""
    address: str = ""
