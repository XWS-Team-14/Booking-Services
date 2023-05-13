from datetime import datetime 
import uuid

from app.models import holiday

async def init_holidays():
    await holiday.Holiday(id=uuid.uuid4(),date=datetime(year=2023,month=5,day=23),title="Family Day").insert()
    await holiday.Holiday(id=uuid.uuid4(),date=datetime(year=2023,month=5,day=30),title="Family Day").insert()
    await holiday.Holiday(id=uuid.uuid4(),date=datetime(year=2023,month=7,day=2),title="Family Day").insert()
    await holiday.Holiday(id=uuid.uuid4(),date=datetime(year=2023,month=1,day=1),title="Sleepo Day").insert()
    await holiday.Holiday(id=uuid.uuid4(),date=datetime(year=2023,month=12,day=31),title="New Years Day").insert()
    await holiday.Holiday(id=uuid.uuid4(),date=datetime(year=2023,month=9,day=23),title="Helloween-ish").insert()