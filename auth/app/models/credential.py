import uuid

from beanie import Document, Indexed
from pydantic import EmailStr

from app.models.role import Role


class Credential(Document):
    id: uuid.UUID
    email: Indexed(EmailStr, unique=True)
    password: str
    role: Role
    active: bool = True
