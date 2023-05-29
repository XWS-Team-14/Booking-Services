from typing import List

from pydantic import BaseModel


class DateInterval(BaseModel):
    date_start: str
    date_end: str


class SpecialPricing(BaseModel):
    title: str
    pricing_markup: float


class AvailabilityDto(BaseModel):
    availability_id: str
    accomodation_id: str
    interval: DateInterval
    pricing_type: str
    base_price: float
    special_pricing: List[SpecialPricing]
    occupied_intervals: List[DateInterval]


class SearchDetails(BaseModel):
    interval: DateInterval
    num_of_guests: int


class PriceLookup(BaseModel):
    interval: DateInterval
    guests: int
    accommodation_id: str
