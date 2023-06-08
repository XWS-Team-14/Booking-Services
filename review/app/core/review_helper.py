import json

from kafka import KafkaConsumer

from app.constants import kafka_server
from app.core import listen_to_reservations


class ReviewHelper:
    async def listen(self):
        await listen_to_reservations()
