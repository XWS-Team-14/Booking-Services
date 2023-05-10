import uuid
from datetime import datetime

from beanie import Document

from .reservation_status import ReservationStatus


class Reservation(Document):
    id: uuid.UUID
    accommodation_id: uuid.UUID
    host_id: uuid.UUID
    # guest who made the reservation
    guest_id: uuid.UUID
    number_of_guests: int
    beginning_date: datetime
    ending_date: datetime
    total_price: float
    status: ReservationStatus

    class Settings:
        indexes = [
            "reservation_id"
        ]
