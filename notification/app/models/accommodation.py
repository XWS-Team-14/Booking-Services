from pydantic import BaseModel


class Accommodation(BaseModel):
    id: str
    name: str
