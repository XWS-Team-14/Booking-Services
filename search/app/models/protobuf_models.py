from pydantic import BaseModel
from pydantic import UUID4


class Location(BaseModel):
    country: str = ""
    city: str = ""
    address: str = ""


class Interval(BaseModel):
    date_start: str = ""
    date_end: str = ""


class Response(BaseModel):
    message_string: str
    status_code: int


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


class ResponseAccommodations(BaseModel):
    response: Response = Response.construct()
    items: list[Accommodation] = []


class SearchParamsAccommodation(BaseModel):
    location: Location
    guests: int = 0


class SearchParams(BaseModel):
    location: Location
    guests: int = 0
    interval: Interval


class SpecialPricing(BaseModel):
    title: str
    pricing_markup: float


class ExpandedAvailabilityDto(BaseModel):
    availability_id: UUID4
    accommodation_id: UUID4
    interval: Interval = Interval.construct()
    pricing_type: str = ""
    base_price: float = 0
    total_price: float = 0
    special_pricing: list[SpecialPricing] = []
    occupied_intervals: list[Interval] = []


class ExpandedAvailabilityDtos(BaseModel):
    items: list[ExpandedAvailabilityDto] = []
