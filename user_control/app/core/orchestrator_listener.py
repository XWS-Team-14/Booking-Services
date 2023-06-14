import asyncio
from aiokafka import AIOKafkaConsumer
from loguru import logger
import uuid
from app.models.user import User
from app.models.deleted_user import DeletedUser
import json
from datetime import datetime

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
            logger.info(message.value)
            if message.value['action'] == 'commit':
                logger.info("Recieved deletion message")
                if message.value['item']:
                    item = await User.find(User.id == uuid.UUID(message.value['item'])).first_or_none()
                    logger.info(item)
                    if not item:  
                        logger.info("Document with given id not found, non deleted")
                        #produce success message
                        kafka_producer.send('orchestrator-responces', {
                            'transaction_id': str(message.value['transaction_id']),
                            'source':'user_control',
                            'status': 'success'                                  
                        })
                    else:
                        logger.info("Delete is possible, deleting")
                        await item.delete()
                        #store it in seperate collection
                        deleted = DeletedUser(
                            item = item,
                            transaction_id = message.value['transaction_id'],
                            timestamp = datetime.utcnow()
                        )
                        await deleted.insert()
                        logger.success("Deleted User succesfully saved")
                        #produce success message
                        kafka_producer.send('orchestrator-responces', {
                            'transaction_id': str(message.value['transaction_id']),
                            'source':'user_control',
                            'status': 'success'                                  
                        })
            elif message.value['action'] == 'rollback':
                logger.info("Recieved rollback message")
                deleted_user = await DeletedUser.find(DeletedUser.transaction_id == uuid.UUID(message.value['transaction_id'])).first_or_none()
                if deleted_user:
                    logger.info("Fetched deleted user, reinserting...")
                    await User.insert(deleted_user.item)
                    logger.info("Reinserted user")
                logger.info("Fetching failed, documents not reinserted")
            else:
                logger.info("Message is malformed, missing command argument - ignoring")
    finally:
        await consumer.stop()
