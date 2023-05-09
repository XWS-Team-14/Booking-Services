from pydantic import BaseModel
import datetime

class Interval(BaseModel):
    date_start: datetime
    date_end: datetime