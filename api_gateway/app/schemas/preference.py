from pydantic import BaseModel


class Preference(BaseModel):
    id: str
    type: str
    enabled: bool
    user_id: str
