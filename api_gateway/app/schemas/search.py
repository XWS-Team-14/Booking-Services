from pydantic import BaseModel, UUID4


class DateInterval(BaseModel):
    date_start: str
    date_end: str


class Location(BaseModel):
    country: str = ""
    city: str = ""
    address: str = ""


class SearchParams(BaseModel):
    interval: DateInterval
    location: Location
    guests: int
    amenities: list[str] = []
    price_min: float = 0
    price_max: float = float('inf')
    must_be_featured_host: bool = False



class SearchResult(BaseModel):
    accommodation_id: UUID4
    host_id: UUID4
    name: str = ""
    location: Location = Location.construct()
    features: list[str] = []
    image_urls: list[str] = []
    min_guests: int = 0
    max_guests: int = 0
    base_price: float = 0
    total_price: float = 0
    auto_accept_flag: bool = False


class Response(BaseModel):
    message_string: str
    status_code: int


class SearchResults(BaseModel):
    response: Response = Response.construct()
    items: list[SearchResult] = []
