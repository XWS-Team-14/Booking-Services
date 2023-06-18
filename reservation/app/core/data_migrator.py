from datetime import datetime, timedelta, time
from app.constants import kafka_producer, kafka_server
from loguru import logger
import asyncio

from app.models.reservation import Reservation
async def start_data_migrator():
    loop = asyncio.get_event_loop()
    while True:
        logger.info("Scheduled task for data migration is triggered, fetching reservations")
        reservations = await Reservation.find(fetch_links=True).to_list()
        total_reservations = len(reservations)
        count = 1
        if total_reservations == 0:
            logger.info("No data found, none sent")  
        for reservation in reservations:
            processed = {
                "accommodation" : str(reservation.accommodation.id),
                "guest" : str(reservation.guest.id),
            }
            #sending one reservation per message due to kafka message size limit of 1mb, could mby pack more but this is ok
            logger.info(f"Prepared reservation:{count} of {total_reservations} for transport")
            kafka_producer.send('data-migration', {
                'data': processed,
                'reset' : 'true' if count == 1 else 'false',
                'date' : datetime.now().date().strftime("%Y-%m-%d"),
                'source' : 'reservation'
            })
            logger.info(f"Sent data {count} of {total_reservations}")
            count += 1
            
        today = datetime.now().date()
        desired_time = time(3, 15)  # 3:15 AM
        logger.info(desired_time)
        desired_datetime = datetime.combine(today, desired_time)
        logger.info(desired_datetime)
        time_difference = (desired_datetime - datetime.now()).total_seconds()
        if time_difference < 0 :
            #current time is after 3:15 AM, wait untill tomorow
            desired_datetime = desired_datetime + timedelta(days=1)
            time_difference = (desired_datetime - datetime.now()).total_seconds()
        logger.info(desired_datetime)
        logger.info(f'Waiting for {time_difference} seconds until next send')
        await asyncio.sleep(time_difference,loop=loop)