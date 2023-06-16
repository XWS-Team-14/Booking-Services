import asyncio
from aiokafka import AIOKafkaConsumer
from loguru import logger
from datetime import datetime
from app.constants import kafka_server,kafka_producer
from app.models.models import User,Accommodation
from neomodel import db, clear_neo4j_database
import json

async def listen_to_migrate_messages():
    logger.info('Listening for migration messages')
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer('data-migration', loop=loop,
                                bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))
    #fetched_date = datetime.now()
    reset_flag = False
    await consumer.start() 
    try:
        async for message in consumer:
            logger.info('Recived migration message')
            if message.value['reset'] == 'true': 
                if reset_flag == False:
                    logger.info('1st message of 1st batch recieved, flush database')
                    #fetched_date = datetime.strptime(message.value['date'], "%Y-%m-%d")
                    reset_flag = True
                    #commit db flush
                    clear_neo4j_database(db)
                    logger.info('Database flushed')
                else:
                    #seccond reset flag came, aka 1st mesage from 2nd source thats all reset flags for today
                    reset_flag = False
                    logger.info('1st message of 2nd batch recieved, reseting reset_flag, ready for next batches tomorow')
                    
            stored_user = User.nodes.get_or_none(user_id = message.value['data']['guest'])
            stored_accommodation = Accommodation.nodes.get_or_none(accomodation_id = message.value['data']['accommodation'])
            if stored_user == None:
                stored_user = User(user_id = message.value['data']['guest'])
                stored_user.save()
                logger.info('Arrived user is not in database, saving')
            if  stored_accommodation == None:
                stored_accommodation = Accommodation(accomodation_id = message.value['data']['accommodation'])
                stored_accommodation.save()
                logger.info('Arrived accommodation is not in database, saving')
                
            if message.value['source'] == 'reservation':
                if not stored_user.reserved.is_connected(stored_accommodation):
                    stored_user.reserved.connect(stored_accommodation)       
                    stored_accommodation.is_reserved.connect(stored_user)
                    logger.info('Reservation between user and accomodation does not exist, saving')
            elif message.value['source'] == 'review':
                if not stored_user.reviewed.is_connected(stored_accommodation):
                    rel = stored_user.reviewed.connect(stored_accommodation)
                    rel.timestamp = datetime.strptime(message.value['data']['date'], "%Y-%m-%d")
                    rel.grade = message.value['data']['grade']
                    rel.save()
                    back_rel = stored_accommodation.is_reviewed.connect(stored_user)
                    back_rel.timestamp = datetime.strptime(message.value['data']['date'], "%Y-%m-%d")
                    back_rel.grade = message.value['data']['grade']
                    back_rel.save()
                    logger.info('Review between user and accomodation does not exist, saving')
                
    finally:
        await consumer.stop()