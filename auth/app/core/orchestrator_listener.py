import asyncio
from aiokafka import AIOKafkaConsumer
from loguru import logger
import uuid
from app.models.credential import Credential
from app.models.deleted_credential import DeletedCredential
import json
from datetime import datetime

from app.constants import kafka_server,kafka_producer


async def listen_to_delete_messages():
    logger.info('Listening for credential deletion messages')
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer("auth-delete", loop=loop,
                                bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))

    await consumer.start()

    try:
        async for message in consumer:
            logger.info(message.value)
            if message.value['action'] == 'commit':
                logger.info("Recieved deletion message")
                if message.value['item']:
                    item = await Credential.find(Credential.id == uuid.UUID(message.value['item'])).first_or_none()
                    logger.info(item)
                    if not item:  
                        logger.info("Document with given id not found, non deleted")
                        #produce success message
                        kafka_producer.send('orchestrator-responces', {
                            'transaction_id': str(message.value['transaction_id']),
                            'source':'auth',
                            'status': 'success'                                  
                        })
                    else:
                        logger.info("Delete is possible, deleting")
                        await item.delete()
                        #store it in seperate collection
                        deleted = DeletedCredential(
                            item = item,
                            transaction_id = message.value['transaction_id'],
                            timestamp = datetime.utcnow()
                        )
                        await deleted.insert()
                        logger.success("Deleted Credentails succesfully saved")
                        #produce success message
                        kafka_producer.send('orchestrator-responces', {
                            'transaction_id': str(message.value['transaction_id']),
                            'source':'auth',
                            'status': 'success'                                  
                        })
            elif message.value['action'] == 'rollback':
                logger.info("Recieved rollback message")
                deleted_user = await DeletedCredential.find(DeletedCredential.transaction_id == uuid.UUID(message.value['transaction_id'])).first_or_none()
                if deleted_user:
                    logger.info("Fetched deleted user, reinserting...")
                    await Credential.insert(deleted_user.item)
                    logger.info("Reinserted user")
                logger.info("Fetching failed, documents not reinserted")
            else:
                logger.info("Message is malformed, missing command argument - ignoring")
    finally:
        await consumer.stop()
