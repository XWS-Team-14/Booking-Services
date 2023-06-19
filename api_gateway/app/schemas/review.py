from pydantic import BaseModel


class CreateReview(BaseModel):
    host_id: str
    accommodation_id: str
    host_rating: int
    accommodation_rating: int

class UpdateReviewDto(BaseModel):
    id: str
    host_rating: int
    accommodation_rating: int
