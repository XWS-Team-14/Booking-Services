import asyncio
from aiokafka import AIOKafkaConsumer
from app.models.availability import Availability
from app.models.deleted_availabilities import DeletedAvailability
from loguru import logger
from datetime import datetime
import json

from app.constants import kafka_server,kafka_producer

async def listen_to_delete_messages():
    logger.info('Listening for availability deletion messages')
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer("availability-delete", loop=loop,
                                bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))

    await consumer.start()

    try:
        async for message in consumer:
            if message.value.command == 'commit':
                logger.info("Recieved deletion message")
                if message.value.items:
                    for avail_id in message.value.items:
                        item = await Availability.get(avail_id)
                        logger.info(item)
                        if not item:
                            logger.info("Delete failed, document with given id not found")
                            #produce fail message
                            kafka_producer.send('orchestrator-responces', {
                                'transaction_id': str(message.value.transaction_id),
                                'source':'availability',
                                'status': 'fail'                                  
                            })
                        if item.occupied_intervals:
                            logger.info("Delete failed, availability has reservations")
                            #produce fail message
                            kafka_producer.send('orchestrator-responces', {
                                'transaction_id': str(message.value.transaction_id),
                                'source':'availability',
                                'status': 'fail'                                  
                            })
                        else:
                            logger.info("Delete is possible, deleting")
                            await item.delete()
                            #store it in seperate collection
                            deleted = DeletedAvailability(
                                item = item,
                                transaction_id = message.value.transaction_id,
                                timestamp = datetime.utcnow()
                            )
                            await deleted.insert()
                            logger.success("Deleted Availability succesfully saved")
                            #produce success message
                            kafka_producer.send('orchestrator-responces', {
                                'transaction_id': str(message.value.transaction_id),
                                'source':'availability',
                                'status': 'success'                                  
                            })
            elif message.value.command == 'rollback':
                logger.info("Recieved rollback message")
                deleted_avails = await DeletedAvailability.find(DeletedAvailability.transaction_id == message.value.transaction_id).to_list()
                if deleted_avails:
                    logger.info("Fetched deleted availabilities, reinserting...")
                    deleted_items = []
                    for del_avail in deleted_avails:
                        deleted_items.append(del_avail.item)
                    await Availability.insert_many(deleted_items)
                    logger.info("Reinserted availabilities")
                logger.info("Fetching failed, documents not reinserted")
            else:
                logger.info("Message is malformed, missing command argument - ignoring")
    finally:
        await consumer.stop()
