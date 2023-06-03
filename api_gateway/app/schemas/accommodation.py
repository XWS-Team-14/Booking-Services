from pydantic import BaseModel
from pydantic import UUID4


class Location(BaseModel):
    country: str = ""
    city: str = ""
    address: str = ""


class Accommodation(BaseModel):
    id: UUID4
    host_id: UUID4
    name: str
    location: Location
    features: list[str]
    image_urls: list[str]
    min_guests: int
    max_guests: int
    auto_accept_flag: bool = False


class Response(BaseModel):
    message_string: str
    status_code: int


class InputId(BaseModel):
    id: str


class ResponseAccommodations(BaseModel):
    response: Response = Response.construct()
    items: list[Accommodation] = []


class ResponseAccommodation(BaseModel):
    response: Response
    item: Accommodation
