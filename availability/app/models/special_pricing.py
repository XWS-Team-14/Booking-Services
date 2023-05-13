from pydantic import BaseModel

class SpecialPricing(BaseModel):
    title: str
    pricing_markup: float