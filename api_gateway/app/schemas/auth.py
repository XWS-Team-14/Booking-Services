import uuid

from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str


class Register(BaseModel):
    first_name: str
    last_name: str
    gender: str
    role: str
    home_address: str
    email: EmailStr
    password: str


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str
    new_password_check: str
