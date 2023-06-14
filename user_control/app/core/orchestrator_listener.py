import asyncio
from aiokafka import AIOKafkaConsumer
from loguru import logger
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
            if message.value.command == 'commit':
                logger.info("Recieved deletion message")
                logger.info(message.value)
                if message.value.item:
                    item = await User.get(message.value.item)
                    logger.info(item)
                    if not item:  
                        logger.info("Delete failed, document with given id not found")
                        #produce fail message
                        kafka_producer.send('orchestrator-responces', {
                            'transaction_id': str(message.value.transaction_id),
                            'source':'user_control',
                            'status': 'fail'                                  
                        })
                    else:
                        logger.info("Delete is possible, deleting")
                        #await item.delete()
                        #store it in seperate collection
                        deleted = DeletedUser(
                            item = item,
                            transaction_id = message.value.transaction_id,
                            timestamp = datetime.utcnow()
                        )
                        await deleted.insert()
                        logger.success("Deleted User succesfully saved")
                        #produce success message
                        kafka_producer.send('orchestrator-responces', {
                            'transaction_id': str(message.value.transaction_id),
                            'source':'user_control',
                            'status': 'success'                                  
                        })
            elif message.value.command == 'rollback':
                logger.info("Recieved rollback message")
                deleted_user = await DeletedUser.get(message.value.item)
                if deleted_user:
                    logger.info("Fetched deleted user, reinserting...")
                    await User.insert(deleted_user.item)
                    logger.info("Reinserted user")
                logger.info("Fetching failed, documents not reinserted")
            else:
                logger.info("Message is malformed, missing command argument - ignoring")
    finally:
        await consumer.stop()
