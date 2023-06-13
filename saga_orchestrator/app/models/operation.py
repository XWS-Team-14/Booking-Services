from enum import Enum

class OperationEnum(str, Enum):
    delete = 'delete'
    rollback = 'rollback'