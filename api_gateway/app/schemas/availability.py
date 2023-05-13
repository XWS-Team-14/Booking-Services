from pydantic import BaseModel
from datetime import datetime
from typing import List

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
    special_pricing:List[SpecialPricing]
    occupied_intervals :List[DateInterval]
    