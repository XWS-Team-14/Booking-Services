from pydantic import BaseModel
from .accommodation import Accommodation
from .location import Location


class Response(BaseModel):
    message_string: str
    status_code: int


class InputId(BaseModel):
    id: str


class ResponseAccommodations(BaseModel):
    response: Response
    items: list[Accommodation]


class ResponseAccommodation(BaseModel):
    response: Response
    item: Accommodation


class SearchParams(BaseModel):
    location: Location
    guests: int = 0
