import asyncio
from aiokafka import AIOKafkaConsumer
from loguru import logger
import json

from app.constants import kafka_server,kafka_producer

async def listen_to_delete_messages():
    logger.info('Listening for user deletion messages')
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer("user-delete", loop=loop,
                                bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))

    await consumer.start()

    try:
        async for message in consumer:
            update = message.value
            logger.info("Recieved deletion message")
            logger.info(message.value)
    finally:
        await consumer.stop()
