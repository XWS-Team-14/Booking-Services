import uuid
from datetime import datetime

from typing import Optional
from pydantic import Field
from beanie import Document, Link


from .accommodation import Accommodation
from .guest import Guest
from .reservation_status import ReservationStatus


class Reservation(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    accommodation: Accommodation
    host_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    # guest who made the reservation
    guest: Link[Guest]
    number_of_guests: int
    beginning_date: datetime
    ending_date: datetime
    total_price: float
    status: ReservationStatus

    class Settings:
        indexes = [
            "id",
        ]
        use_state_management = True
        state_management_replace_objects = True
