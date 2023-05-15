import uuid
from datetime import datetime

from beanie import Document

from .accommodation import Accommodation
from .guest import Guest
from .reservation_status import ReservationStatus


class Reservation(Document):
    id: uuid.UUID
    accommodation: Accommodation
    host_id: uuid.UUID
    # guest who made the reservation
    guest: Guest
    number_of_guests: int
    beginning_date: datetime
    ending_date: datetime
    total_price: float
    status: ReservationStatus

    class Settings:
        indexes = [
            "id"
        ]