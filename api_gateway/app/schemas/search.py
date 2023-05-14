from pydantic import BaseModel


class DateInterval(BaseModel):
    date_start: str
    date_end: str


class Location(BaseModel):
    country: str
    city: str
    address: str


class SearchParams(BaseModel):
    interval: DateInterval
    location: Location
    guests: int
