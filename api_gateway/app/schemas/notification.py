from pydantic import BaseModel


class Receiver(BaseModel):
    id: str


class Sender(BaseModel):
    id: str
    name: str


class Notification(BaseModel):
    type: str
    title: str
    content: str
    sender: Sender
    receiver: Receiver
    status: str
    timestamp: str
