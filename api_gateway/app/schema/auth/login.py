from pydantic import EmailStr, BaseModel


class Login(BaseModel):
    email: EmailStr
    password: str