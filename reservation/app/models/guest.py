import uuid

from beanie import Document
from pydantic import BaseModel


class Guest (BaseModel):
    guest_id : uuid.UUID
    canceledReservations : int

