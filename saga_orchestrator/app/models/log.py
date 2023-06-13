import uuid
from beanie import Document
from datetime import datetime

from saga_orchestrator.app.models.log_type import LogTypeEnum
from saga_orchestrator.app.models.operation import OperationEnum
from saga_orchestrator.app.models.status import StatusEnum

class Log(Document):
    id: uuid.UUID
    transaction_id: uuid.UUID
    log_type:LogTypeEnum
    timestamp: datetime
    operation: OperationEnum
    target: str
    status: StatusEnum
    objects: any

    class Settings:
        indexes = [
            "id",
            "transaction_id"
        ]
