import uuid
from pydantic import UUID4
from beanie import Document
from datetime import datetime
from typing import Any

from app.models.log_type import LogTypeEnum
from app.models.operation import OperationEnum
from app.models.status import StatusEnum

class Log(Document):
    id: UUID4
    transaction_id: UUID4
    log_type:LogTypeEnum
    timestamp: datetime
    operation: OperationEnum
    target: str
    status: StatusEnum
    objects: Any

    class Settings:
        indexes = [
            "id",
            "transaction_id"
        ]
