
import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel

class Guest(BaseModel):
    id: uuid.UUID
    canceledReservations : int

class Accommodation (BaseModel):
    id:uuid.UUID
    automaticAccept: bool

class ReservationDto(BaseModel):
    reservation_id: uuid.UUID
    accommodation: Accommodation
    host_id: uuid.UUID
    guest: Guest
    number_of_guests: int
    beginning_date: datetime
    ending_date: datetime
    total_price: float
    status: int
