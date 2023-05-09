import uuid
import datetime
from typing import List
from availability.app.models.interval import Interval
from availability.app.models.pricing_type import PricingTypeEnum
from availability.app.models.special_pricing import SpecialPricing
from beanie import Document


class Availability(Document):
    availability_id: uuid.UUID
    accomodation_id: uuid.UUID
    available_interval: Interval
    pricing_type: PricingTypeEnum
    base_price: float
    special_pricing:List[SpecialPricing]
    occupied_intervals :List[Interval] 
    