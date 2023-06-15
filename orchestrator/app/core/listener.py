import asyncio
from aiokafka import AIOKafkaConsumer
from loguru import logger
from datetime import datetime
from app.models.log import Log
from app.models.status import StatusEnum
import json
import uuid

from app.constants import kafka_server,kafka_producer

async def listen_to_delete_messages():
    logger.info('Listening for saga response messages')
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer("orchestrator-responces", loop=loop,
                                bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))

    await consumer.start()
    try:
        async for message in consumer:
            logger.info("Recieved deletion message")
            logger.info(message)
            log = await Log.find(Log.transaction_id == uuid.UUID(message.value['transaction_id'])).first_or_none()
            if log is None:
                logger.info("Malformed message, transaction_id does not match any stored, ignoring message")
                continue
            if message.value['status'] =='fail':
                logger.info("Failiure message, setting transaciton status as failed")
                log.status = StatusEnum.fail
                await log.replace()
                logger.info("Failiure message, sending out rollback message")
                if message.value['source'] != 'user_control':
                    kafka_producer.send('user-delete', {
                        'transaction_id': str(message.value['transaction_id']),
                        'action': 'rollback' 
                    })
                if message.value['source'] != 'accommodation':
                    kafka_producer.send('accommodation-delete', {
                        'transaction_id': str(message.value['transaction_id']),
                        'action': 'rollback' 
                    })
                if message.value['source'] != 'availability':
                    kafka_producer.send('availability-delete', {
                        'transaction_id': str(message.value['transaction_id'])   ,
                        'action': 'rollback'                                  
                    })
                if message.value['source'] != 'auth':
                    kafka_producer.send('auth-delete', {
                        'transaction_id': str(message.value['transaction_id'])   ,
                        'action': 'rollback'                                  
                    })
            elif message.value['status'] =='success':
                logger.info("Success message, updatating confirmation flag")
                log.confirmations = log.confirmations + 1
                if log.confirmations == 4:
                    logger.info("Transaction has gotten all success responces, updating transaction status as success")
                    log.status = StatusEnum.success
                await log.replace()
                logger.info("Updated transaction log")
                logger.info(log)
    finally:
        await consumer.stop()