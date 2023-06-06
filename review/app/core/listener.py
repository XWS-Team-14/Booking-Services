import uuid

from loguru import logger

from app.constants import kafka_consumer
from app.models.accommodation import Accommodation
from app.models.host import Host
from app.models.message import Message


async def listen_to_reservations():
    logger.info('Listening for reservation updates')
    for message in kafka_consumer:
        update = message.value
        message_id = uuid.UUID(update['id'])
        #existing_message = await Message.find_one(Message.id == message_id)
        #print(existing_message)
        # new_message = Message(id=message_id, status=MessageStatus.NOT_PROCESSED, timestamp=datetime.datetime.utcnow())
        # if existing_message is None or existing_message.status == MessageStatus.NOT_PROCESSED:
        #    await new_message.save()
        #    if update['event'] == 'create':
        #        await handle_new_reservation(message)
        #        new_message.status = MessageStatus.PROCESSED
        #    elif update['event'] == 'cancel':
        #        await handle_cancelled_reservation(message)
        #        new_message.status = MessageStatus.PROCESSED
        #    else:
        #        logger.info(f"Unknown event type for message ID {str(message_id)}")
        #    await new_message.replace()


async def handle_new_reservation(message):
    host = await Host.find_one(Host.id == uuid.UUID(message['host']))
    accommodation = await Accommodation.find_one(Accommodation.id == uuid.UUID(message['accommodation']))
    if host is None:
        host = Host()
    if accommodation is None:
        accommodation = Accommodation()

    original_status = host.is_featured()

    host.increase_reservation_count()
    host.increase_reservation_days(int(message['days']))

    new_status = host.is_featured()
    print(original_status, new_status)

    if original_status != new_status:
        # send message to status channel
        logger.info('Status changed')

    await host.save()
    await accommodation.save()


async def handle_cancelled_reservation(message):
    host = await Host.find_one(Host.id == uuid.UUID(message['host']))
    original_status = host.is_featured()
    host.decrease_reservation_count()
    host.decrease_reservation_days(message['days'])

    new_status = host.is_featured()
    print(original_status, new_status)

    if original_status != new_status:
        # send message to status channel
        logger.info('Status changed')

    await host.save()
