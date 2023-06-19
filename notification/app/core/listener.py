import asyncio
import json
import uuid
from datetime import datetime

from aiokafka import AIOKafkaConsumer
from loguru import logger

from app import db
from app.config import get_yaml_config
from app.core.notification_helper import get_type, generate
from app.models.notification import Notification
from app.models.preference import Preference
from app.models.receiver import Receiver
from app.models.sender import Sender


async def listen():
    logger.info('Listening for status updates')
    loop = asyncio.get_event_loop()
    kafka_server = get_yaml_config().get("kafka_server").get("ip") + ":" + get_yaml_config().get("kafka_server").get(
        "port")
    consumer = AIOKafkaConsumer("status", loop=loop,
                                bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))
    await consumer.start()

    try:
        async for message in consumer:
            message = message.value
            featured = message['featured']
            user_id = message['host']
            ref = db.reference(f'notifications/{user_id}')
            receiver = Receiver(id=user_id)
            notification = Notification(type=get_type('featured-host-gained' if featured else 'featured-host-lost'), status='unread',
                                        timestamp=datetime.now(), sender=None, receiver=receiver,
                                        accommodation=None, title='', content='')
            notification = generate(notification, 'featured-host-gained' if featured else 'featured-host-lost')
            message = json.loads(json.dumps(notification, default=lambda o: o.__dict__))
            user_preferences = await Preference.find(Preference.user.id == user_id).to_list()
            for preference in user_preferences:
                if preference.type == get_type('featured-host-gained' if featured else 'featured-host-lost'):
                    print(preference.enabled)
                    if preference.enabled:
                        ref.push(message)

    finally:
        await consumer.stop()