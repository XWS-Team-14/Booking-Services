import asyncio
import datetime
import json
import uuid

from aiokafka import AIOKafkaConsumer
from loguru import logger

from app.constants import kafka_consumer, kafka_producer, kafka_server
from app.models.accommodation import Accommodation
from app.models.host import Host
from app.models.message import Message
from app.models.message_status import MessageStatus


async def listen_to_reservations():
    logger.info('Listening for reservation updates')
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer("reservations", loop=loop,
                                bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))

    await consumer.start()

    try:
        async for message in consumer:
            update = message.value
            message_id = uuid.UUID(update['id'])
            existing_message = await Message.get(message_id)
            new_message = Message(id=message_id, status=0, timestamp=datetime.datetime.utcnow())
            if existing_message is None or existing_message.status == 0:
                await new_message.save()
                if update['event'] == 'create':
                    await handle_new_reservation(update)
                    new_message.status = 1
                elif update['event'] == 'cancel':
                    await handle_cancelled_reservation(update)
                    new_message.status = 1
                else:
                    logger.info(f"Unknown event type for message ID {str(message_id)}")
                await new_message.replace()
    finally:
        await consumer.stop()


async def handle_new_reservation(message):
    host = await Host.find_one(Host.id == uuid.UUID(message['host']))
    accommodation = await Accommodation.find_one(Accommodation.id == uuid.UUID(message['accommodation']))
    if host is None:
        host = Host(id=uuid.UUID(message['host']))
    if accommodation is None:
        accommodation = Accommodation(id=uuid.UUID(message['accommodation']), host=host)

    original_status = host.is_featured()

    host.increase_reservation_count()
    host.increase_reservation_days(int(message['days']))

    new_status = host.is_featured()
    print(original_status, new_status)

    if original_status != new_status:
        kafka_producer.send('status', {
            'host': str(host.id),
            'featured': new_status,
            'timestamp': str(datetime.datetime.utcnow())
        })

    await host.save()
    await accommodation.save()


async def handle_cancelled_reservation(message):
    host = await Host.find_one(Host.id == uuid.UUID(message['host']))
    original_status = host.is_featured()
    host.decrease_reservation_days(message['days'])

    new_status = host.is_featured()
    print(original_status, new_status)

    if original_status != new_status:
        kafka_producer.send('status', {
            'host': str(host.id),
            'featured': new_status,
            'timestamp': str(datetime.datetime.utcnow())
        })

    await host.save()
