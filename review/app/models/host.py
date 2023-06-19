from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


class Host(Document):
    id: UUID = Field(default_factory=uuid4)
    review_count: int = 0
    rating_sum: int = 0
    cancelled_count: int = 0
    reservation_days: int = 0
    reservation_count: int = 0

    def increase_review_count(self):
        self.review_count += 1

    def decrease_review_count(self):
        self.review_count -= 1

    def increase_rating_sum(self, rating):
        self.rating_sum += rating

    def decrease_rating_sum(self, rating):
        self.rating_sum -= rating

    def increase_reservation_count(self):
        self.reservation_count += 1

    def increase_reservation_days(self, days):
        self.reservation_days += days

    def decrease_reservation_count(self):
        self.reservation_count -= 1

    def decrease_reservation_days(self, days):
        self.reservation_days -= days

    def get_cancellation_rate(self):
        return (self.cancelled_count / self.reservation_count) * 100 if self.reservation_count else 0

    def get_average_rating(self):
        return self.rating_sum / self.review_count if self.review_count else 0

    def is_featured(self):
        return self.get_average_rating() > 4.7 \
            and self.get_cancellation_rate() < 5 <= self.reservation_count \
            and self.reservation_days > 50
