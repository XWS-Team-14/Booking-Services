from app.models.log import Log
from app.models.status import StatusEnum
from datetime import datetime, timedelta
from app.constants import kafka_producer, kafka_server
from loguru import logger
import asyncio


async def no_response_rollback():
    loop = asyncio.get_event_loop()
    while True:
        logger.info("Scheduled task is triggered, fetching transactions")
        logs = await Log.find(
            Log.status == 'sent'
        ).to_list()
        logs = list(filter(lambda log: (log.timestamp + timedelta(minutes=5)) <= datetime.now(), logs))
        if len(logs) == 0:
            logger.info("0 no response transactions found.")
            await asyncio.sleep(5 * 60, loop=loop)
            continue
        for log in logs:
            log.status = StatusEnum.fail
            logger.info("Setting transaction log status to fail and sending rollback")
            kafka_producer.send('user-delete', {
                'transaction_id': str(log.transaction_id),
                'action': 'rollback'
            })
            kafka_producer.send('accommodation-delete', {
                'transaction_id': str(log.transaction_id),
                'action': 'rollback'
            })
            kafka_producer.send('availability-delete', {
                'transaction_id': str(log.transaction_id),
                'action': 'rollback'
            })
            kafka_producer.send('auth-delete', {
                'transaction_id': str(log.transaction_id),
                'action': 'rollback'
            })
            log.replace()
        await asyncio.sleep(5 * 60, loop=loop)
