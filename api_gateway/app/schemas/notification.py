from pydantic import BaseModel


class Receiver(BaseModel):
    id: str


class Sender(BaseModel):
    id: str
    name: str


class Accommodation(BaseModel):
    id: str
    name: str


class Notification(BaseModel):
    type: str
    sender: Sender
    receiver: Receiver
    accommodation: Accommodation
    status: str
    timestamp: str
