from enum import Enum

class StatusEnum(str, Enum):
    sent = 'sent'
    success = 'success'
    fail = 'fail'