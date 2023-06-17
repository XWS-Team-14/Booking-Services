from datetime import datetime, timedelta, time
from app.constants import kafka_producer, kafka_server
from loguru import logger
import asyncio
from app.models.review import Review

async def start_data_migrator():
    loop = asyncio.get_event_loop()
    while True:
        logger.info("Scheduled task for data migration is triggered, fetching reviews")
        
        reviews = await Review.find(fetch_links=True).to_list()
        total_reviews = len(reviews)
        count = 1
        if total_reviews == 0:
            logger.info("No data found, none sent")  
        
        for review in reviews:
            processed = {
                "accommodation" : str(review.accommodation.id),
                "guest" : str(review.poster),
            }
            logger.info(f"Prepared review:{count} of {total_reviews} for transport")
            kafka_producer.send('data-migration', {
                'data': processed,
                'reset' : 'true' if count == 1 else 'false',
                'date' : datetime.now().date().strftime("%Y-%m-%d"),
                'timestamp' : review.timestamp.isoformat(),
                'grade' : review.accommodation_rating,
                'source' : 'review'
            })
            logger.info(f"Sent data {count} of {total_reviews}")
            count += 1
            
        today = datetime.now().date()
        desired_time = time(3, 45)  # 3:45 AM
        logger.info(desired_time)
        desired_datetime = datetime.combine(today, desired_time)
        logger.info(desired_datetime)
        time_difference = (desired_datetime - datetime.now()).total_seconds()
        if time_difference < 0 :
            #current time is after 3:45 AM, wait untill tomorow
            desired_datetime = desired_datetime + timedelta(days=1)
            time_difference = (desired_datetime - datetime.now()).total_seconds()
        logger.info(desired_datetime)
        logger.info(f'Waiting for {time_difference} seconds until next send')
        await asyncio.sleep(time_difference,loop=loop)