from pydantic import BaseModel, UUID4
from .protobuf_models import Location, ExpandedAvailabilityDto, Accommodation


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

    def create(self, acc: Accommodation, avv: ExpandedAvailabilityDto):
        self.accommodation_id = acc.id
        self.host_id = acc.host_id
        self.name = acc.name
        self.location = acc.location
        self.features = acc.features
        self.image_urls = acc.image_urls
        self.min_guests = acc.min_guests
        self.max_guests = acc.max_guests
        self.base_price = avv.base_price
        self.total_price = avv.base_price
        self.auto_accept_flag = acc.auto_accept_flag
        return self


class Response(BaseModel):
    message_string: str = ""
    status_code: int


class SearchResults(BaseModel):
    response: Response = Response.construct()
    items: list[SearchResult] = []
