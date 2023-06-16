import asyncio
from aiokafka import AIOKafkaConsumer
from loguru import logger
import json
import uuid
from datetime import datetime 

from app.models.accommodation import Accommodation
from app.models.deleted_accomodation import DeletedAccommodation
from app.constants import kafka_server,kafka_producer

async def listen_to_delete_messages():
    logger.info('Listening for accomodation deletion messages')
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer("accommodation-delete", loop=loop,
                                bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))

    await consumer.start()

    try:
        async for message in consumer:
            if message.value['action'] == 'commit':
                logger.info("Recieved deletion message")
                logger.info(message.value)
                if message.value['item']:
                    items = await Accommodation.find(Accommodation.host_id == uuid.UUID(message.value['item'])).to_list()
                    if len(items) == 0:  
                        logger.info("No accommodations for host found, none deleted")
                        #produce success message
                        kafka_producer.send('orchestrator-responces', {
                                'transaction_id': str(message.value['transaction_id']),
                                'source':'accommodation',
                                'status': 'success'                                  
                        })
                    else:
                        for item in items:
                            logger.info("Delete is possible, deleting")
                            await item.delete()
                            #store it in seperate collection
                            deleted = DeletedAccommodation(
                                item=item,
                                transaction_id = message.value['transaction_id'],
                                timestamp = datetime.utcnow()
                            )
                            await deleted.insert()
                            logger.success("Deleted Accomodation succesfully saved")
                            #produce success message
                            kafka_producer.send('orchestrator-responces', {
                                'transaction_id': str(message.value['transaction_id']),
                                'source':'accommodation',
                                'status': 'success'                                  
                            })
            elif message.value['action'] == 'rollback':
                logger.info("Recieved rollback message")
                deleted_accommodations = await DeletedAccommodation.find(DeletedAccommodation.transaction_id == uuid.UUID(message.value['transaction_id'])).to_list()
                if len(deleted_accommodations)!=0:
                    logger.info("Fetched deleted accommodation, reinserting...")
                    deleted_items = []
                    for deleted in deleted_accommodations:
                        deleted_items.append(deleted.item)
                    await DeletedAccommodation.insert_many(deleted_items)
                    logger.info("Reinserted accommodation")
                logger.info("Fetching failed, documents not reinserted")
            else:
                logger.info("Message is malformed, missing command argument - ignoring")    
    finally:
        await consumer.stop()
