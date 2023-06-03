from pydantic import BaseModel


class Response(BaseModel):
    message_string: str
    status_code: int
