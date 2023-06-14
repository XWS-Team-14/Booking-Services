import asyncio
from aiokafka import AIOKafkaConsumer
from loguru import logger
from datetime import datetime
import json

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
            if message.value['status'] =='fail':
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
    finally:
        await consumer.stop()