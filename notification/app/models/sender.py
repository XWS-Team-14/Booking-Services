from pydantic import BaseModel


class Sender(BaseModel):
    id: str
    name: str