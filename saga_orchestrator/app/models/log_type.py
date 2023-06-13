from enum import Enum

class LogTypeEnum(str, Enum):
    execute = 'execute'
    response = 'response'