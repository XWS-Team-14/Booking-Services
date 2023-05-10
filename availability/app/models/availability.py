import uuid
from typing import List
from app.models.interval import Interval
from app.models.pricing_type import PricingTypeEnum
from app.models.special_pricing import SpecialPricing
from beanie import Document


class Availability(Document):
    availability_id: uuid.UUID
    accomodation_id: uuid.UUID
    available_interval: Interval
    pricing_type: PricingTypeEnum
    base_price: float
    special_pricing:List[SpecialPricing]
    occupied_intervals :List[Interval] 
    
    class Settings:
        indexes = [
            "availability_id"
        ]
    