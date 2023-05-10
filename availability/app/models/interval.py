from pydantic import BaseModel
from datetime import datetime

class Interval(BaseModel):
    date_start: datetime
    date_end: datetime