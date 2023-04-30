import uuid
from pydantic import BaseModel, EmailStr


class Register(BaseModel):
    email: EmailStr
    password: str
    role: str
    name: str
    surname: str
    home_address: str
