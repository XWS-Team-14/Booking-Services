import uuid
from typing import List
from app.models.interval import Interval
from app.models.pricing_type import PricingTypeEnum
from app.models.special_pricing import SpecialPricing
from beanie import Document
from pydantic import Field


class Availability(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    accomodation_id: uuid.UUID
    available_interval: Interval
    pricing_type: PricingTypeEnum
    base_price: float
    special_pricing:List[SpecialPricing]
    occupied_intervals :List[Interval] 
    
    class Settings:
        indexes = [
            "id"
        ]
    