import uuid

from loguru import logger
from proto import review_pb2_grpc, review_pb2
from datetime import datetime
from app.models.host import Host
from app.models.accommodation import Accommodation
from app.models.review import Review
from .review_helper import ReviewHelper

class ReviewServicer(review_pb2_grpc.ReviewServiceServicer):
    async def GetHostStatus(self, request, context):
        logger.info(f'Fetching host {request.id} status')
        host = await Host.get(uuid.UUID(request.id))

        if host is None:
            return review_pb2.HostStatus(error_message="Host not found", error_code=404)
        else:
            return review_pb2.HostStatus(id=request.id, status=host.is_featured())

    async def CreateReview(self, request, context):
        logger.info('Creating review')
        if request is None:
            logger.info('request is none')
            raise TypeError
        host = await Host.get(uuid.UUID(request.host_id))
        logger.info('host fetched')
        if host is None:
            return review_pb2.ReviewResponse(review=None, message="Host not found", code=404)
        logger.info('Host Found')
        accommodation = await Accommodation.get(uuid.UUID(request.accommodation_id))
        if accommodation is None:
            return review_pb2.ReviewResponse(review=None, message="Accommodation not found", code=404)
        logger.info('Accommodation found')
        review = Review(
                        id=uuid.UUID(request.id),
                        host=host,
                        accommodation=accommodation,
                        poster=request.poster,
                        timestamp=datetime.today(),
                        host_rating=request.host_rating,
                        accommodation_rating=request.accommodation_rating
                        )
        await review.insert()
        logger.info("Inserted review")
        host.increase_review_count()
        host.increase_rating_sum(request.host_rating)
        logger.info("incresed sum and count")
        await host.replace()
        logger.info("replaced host")
        accommodation.review_count += 1
        accommodation.rating_sum+= request.accommodation_rating
        logger.info("incresed sum and count")
        await accommodation.replace()
        logger.info("replaced accommodation")
        return review_pb2.ReviewResponse(review=ReviewHelper.convertReviewToDto(review), message="Review saved", code=200)

    async def GetAllReviews(self, request, context):
        logger.success('Request for fetch all reviews accepted')
        reviews = await Review.find_all(fetch_links=True).to_list()
        retVal = review_pb2.ReviewDtos()
        logger.info('fetched data converting')
        for review in reviews:
            retVal.items.append(ReviewHelper.convertReviewToDto(review))
        logger.success('Succesfully fetched')
        return retVal

    async def GetReviewsByHost(self, request, context):
        logger.success('Request for fetching reviews by host accepted')
        reviews = await Review.find_all(fetch_links=True).to_list()
        retVal = review_crud_pb2.ReviewDtos()
        for review in reviews:
            if review.host.id == request.id:
                retVal.items.append(ReviewHelper.convertReviewToDto(review))
        return retVal

    async def GetReviewById(self, request, context):
        logger.success('Request for fetch review accepted')
        try:
            item = await Review.find_one(Review.id == uuid.UUID(request.id), fetch_links=True)
        except (ValueError, DocumentNotFound):
            logger.info('Fetch failed, document with given id not found')
            return review_pb2.Review()
        if not item:
            logger.info('fetched nothing')
            return review_pb2.Review()
        else:
            logger.success('Succesfully fetched')
            return ReviewHelper.convertReviewToDto(item)


    async def UpdateReview(self, request, context):
        logger.success('Request for update of review accepted')
        try:
            item = await Reservation.get(uuid.UUID(request.id), fetch_links=True)
            if not item:
                logger.info('Update failed, document with given id not found')
                return review_pb2.ReservationResult(status="Failed, not found")
            item.host.increase_rating_sum(request.host_rating - item.host_rating)
            item.host.replace()
            item.accommodation.rating_sum += (request.accommodation_rating - item.accommodation_rating)
            item.accommodation.replace()
            item.timestamp = datetime.today()
            item.host_rating = request.host_rating
            item.accommodation_rating = request.accommodation_rating
            await item.replace()
        except (ValueError, DocumentNotFound):
            logger.info('Update failed, document with given id not found')
            return review_pb2.Empty(error_message="Failed, not found", error_code = 404)
        logger.success('Reservation succesfully updated')
        return review_pb2.ReservationResult(review=ReviewHelper.convertReviewToDto(item),message="Success", code=200)

    async def Delete(self, request, context):
        logger.success('Request for cancellation of Reservation accepted')
        try:
            item = await Reservation.get(uuid.UUID(request.id), fetch_links=True)
            if not item:
                logger.info('Delete failed, document with given id not found')
                return review_pb2.Reservation()
        except (ValueError, DocumentNotFound):
            logger.info('Delete failed, document with given id not found')
            return review_pb2.Reservation()
        item.host.decrease_rating_count()
        item.host.increase_rating_sum(-item.host_rating)
        item.accommodation.rating_count -= 1
        item.accommodation.rating_sum -= item.accommodation_rating
        await item.host.replace()
        await item.accommodation.replace()
        await item.delete()

        logger.success('reservation succesfully deleted')
        return review_pb2.Empty(error_message="Success", error_code = 200)