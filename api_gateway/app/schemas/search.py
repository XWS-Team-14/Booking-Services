from pydantic import BaseModel, UUID4


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


class SearchResult(BaseModel):
    accommodation_id: UUID4
    host_id: UUID4
    name: str
    location: Location
    features: list[str]
    image_urls: list[str]
    min_guests: int
    max_guests: int
    base_price: float
    total_price: float
    auto_accept_flag: bool


class Response(BaseModel):
    message_string: str
    status_code: int


class SearchResults(BaseModel):
    response: Response = Response.construct()
    items: list[SearchResult] = []
