import json

from kafka import KafkaConsumer
from loguru import logger
from app.constants import kafka_server
from app.core import listen_to_reservations
from proto import review_pb2_grpc, review_pb2

class ReviewHelper:
    async def listen(self):
        await listen_to_reservations()


    def convertReviewToDto(review):
        retVal = review_pb2.Review()
        retVal.id = str(review.id)
        retVal.host_id = str(review.host.id)
        retVal.accommodation_id = str(review.accommodation.id)
        retVal.poster = review.poster
        retVal.timestamp = review.timestamp.isoformat().split('T')[0]
        retVal.host_rating = review.host_rating
        retVal.accommodation_rating = review.accommodation_rating
        return retVal



    def convertDateTime(datetime):
        # '2019-05-18T15:17:08.132263'
        return datetime.isoformat().split('T')[0]