import uuid
from beanie import Document, Indexed
from pydantic import EmailStr


class Credential(Document):
    id: uuid.UUID = uuid.uuid4()
    email: Indexed(EmailStr, unique=True)
    password: str
    active: bool = True
