import uuid
from beanie import Document


class Question(Document):
    question_id: uuid.UUID
    credit: int
    title: str
    contest_name: str

    class Settings:
        indexes = [
            "question_id",
            "title_slug",
            "contest_name",
        ]
