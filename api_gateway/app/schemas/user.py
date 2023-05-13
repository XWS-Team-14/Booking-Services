from pydantic import BaseModel, EmailStr


class UserDetailsUpdate(BaseModel):
    first_name: str
    last_name: str
    gender: str
    home_address: str

class User(BaseModel):
    first_name: str
    last_name: str
    gender: str
    home_address: str