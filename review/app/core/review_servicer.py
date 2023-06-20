import uuid

from beanie.exceptions import DocumentNotFound
from loguru import logger
from proto import review_pb2_grpc, review_pb2
from datetime import datetime

from app.models.accommodation import Accommodation
from app.models.host import Host
from app.models.accommodation import Accommodation
from app.models.review import Review
from .review_helper import ReviewHelper
from ..constants import kafka_producer


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
        host = await Host.get(uuid.UUID(request.host_id))
        if host is None:
            host = Host(id=uuid.UUID(request.host_id))
            host = await host.insert()
        print('Host found')
        accommodation = await Accommodation.get(uuid.UUID(request.accommodation_id))
        if accommodation is None:
            accommodation = Accommodation(id=uuid.UUID(request.accommodation_id), host=host)
            accommodation = await accommodation.insert()
        logger.info('Accommodation found')

        original_status = host.is_featured()
        review = Review(
            id=uuid.UUID(request.id),
            host=host,
            accommodation=accommodation,
            poster=request.poster,
            timestamp=datetime.now(),
            host_rating=request.host_rating,
            accommodation_rating=request.accommodation_rating
        )
        await review.insert()
        logger.info("Inserted review")
        host.increase_review_count()
        host.increase_rating_sum(request.host_rating)
        logger.info("increased sum and count")
        await host.replace()
        logger.info("replaced host")
        accommodation.review_count += 1
        accommodation.rating_sum += request.accommodation_rating
        logger.info("increased sum and count")
        await accommodation.replace()
        logger.info("replaced accommodation")

        new_status = host.is_featured()
        print(original_status, new_status)

        if original_status != new_status:
            kafka_producer.send('status', {
                'host': str(host.id),
                'featured': new_status,
                'timestamp': str(datetime.utcnow())
            })
        return review_pb2.AverageRatings(host_average=host.get_average_rating(), accommodation_average=accommodation.get_average_rating())

    async def GetAllReviews(self, request, context):
        logger.success('Request for fetch all reviews accepted')
        reviews = await Review.find_all(fetch_links=True).to_list()
        retVal = review_pb2.ReviewDtos()
        logger.info('fetched data converting')
        for review in reviews:
            retVal.items.append(ReviewHelper.convertReviewToDto(review))
        logger.success('Successfully fetched')
        return retVal

    async def GetReviewsByHost(self, request, context):
        logger.success('Request for fetching reviews by host accepted')
        reviews = await Review.find_all(fetch_links=True).to_list()
        retVal = review_pb2.ReviewDtos()
        for review in reviews:
            if str(review.host.id) == request.id:
                retVal.items.append(ReviewHelper.convertReviewToDto(review))
                logger.info("Appended it")
        return retVal

    async def GetReviewsByPoster(self, request, context):
        logger.success('Request for fetching reviews by poster accepted')
        reviews = await Review.find_all(fetch_links=True).to_list()
        retVal = review_pb2.ReviewDtos()
        for review in reviews:
            if str(review.poster) == request.id:
                retVal.items.append(ReviewHelper.convertReviewToDto(review))
                logger.info("Appended it")
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
        item = await Review.get(uuid.UUID(request.id), fetch_links=True)
        if not item:
            logger.info('Update failed, document with given id not found')
            return review_pb2.Empty(error_message="Failed, not found", error_code=404)
        host = await Host.get(item.host.id)
        if host is None:
            return review_pb2.Empty(error_message="Failed, not found", error_code=404)
        original_status = host.is_featured()
        logger.info("before edit: " + str(host.rating_sum))
        host.increase_rating_sum(request.host_rating - item.host_rating)
        logger.info("After edit: " + str(host.rating_sum))
        await host.replace()
        accommodation = await Accommodation.get(item.accommodation.id)
        if accommodation is None:
            return review_pb2.Empty(error_message="Failed, not found accomm", error_code=404)
        logger.info("before edit accom: " + str(accommodation.rating_sum))
        accommodation.rating_sum += (request.accommodation_rating - item.accommodation_rating)
        logger.info("after edit accom: " + str(accommodation.rating_sum))
        await accommodation.replace()

        item.timestamp = datetime.today()
        item.host_rating = request.host_rating
        item.accommodation_rating = request.accommodation_rating
        await item.replace()
        logger.success('Review succesfully updated')
        new_status = host.is_featured()
        print(original_status, new_status)

        if original_status != new_status:
            kafka_producer.send('status', {
                'host': str(host.id),
                'featured': new_status,
                'timestamp': str(datetime.utcnow())
            })
        return review_pb2.AverageRatings(host_average=host.get_average_rating(), accommodation_average=accommodation.get_average_rating())


    async def DeleteReview(self, request, context):
        logger.success('Request for cancellation of Review accepted')
        try:
            item = await Review.get(uuid.UUID(request.id), fetch_links=True)
            if not item:
                logger.info('Delete failed, document with given id not found')
                return review_pb2.Review()
        except (ValueError, DocumentNotFound):
            logger.info('Delete failed, document with given id not found')
            return review_pb2.Review()

        original_status = item.host.is_featured()
        item.host.decrease_review_count()
        item.host.decrease_rating_sum(item.host_rating)
        item.accommodation.review_count -= 1
        item.accommodation.rating_sum -= item.accommodation_rating
        await item.host.replace()
        await item.accommodation.replace()
        await item.delete()

        logger.success('review successfully deleted')
        new_status = item.host.is_featured()
        print(original_status, new_status)

        if original_status != new_status:
            kafka_producer.send('status', {
                'host': str(item.host.id),
                'featured': new_status,
                'timestamp': str(datetime.utcnow())
            })
        return review_pb2.AverageRatings(host_average=item.host.get_average_rating(), accommodation_average=item.accommodation.get_average_rating())

    async def GetAllAccommodationsWithFeaturedHost(self, request, context):
        all_accommodations = await Accommodation.find_all(fetch_links=True).to_list()
        featured_accommodations = []
        print(all_accommodations)
        for accommodation in all_accommodations:
            if accommodation.host.is_featured():
                featured_accommodations.append(str(accommodation.id))
        print(featured_accommodations)
        print(review_pb2.Accommodations(accommodation_id=featured_accommodations))

        return review_pb2.Accommodations(accommodation_id=featured_accommodations)

    async def GetReviewsByAccommodation(self, request, context):
        logger.success('Request for fetching reviews by accommodation accepted')
        reviews = await Review.find_all(fetch_links=True).to_list()
        retVal = review_pb2.ReviewDtos()
        accommodation = await Accommodation.get(uuid.UUID(request.id), fetch_links=True)
        if accommodation is None:
            return review_pb2.ReviewDtos(items=[], accommodation_average=0, host_average=0)
        host = accommodation.host
        for review in reviews:
            if str(review.accommodation.id) == request.id:
                retVal.items.append(ReviewHelper.convertReviewToDto(review))
                logger.info("Appended it")

        retVal.accommodation_average = accommodation.get_average_rating()
        retVal.host_average = host.get_average_rating()
        return retVal

    async def CreateHostAndAccommodation(self, request, context):
        host = await Host.get(uuid.UUID(request.host_id))
        if host is None:
            host = Host(id=uuid.UUID(request.host_id))
            host = await host.insert()
        accommodation = Accommodation(id=uuid.UUID(request.accommodation_id), host=host)
        accommodation = await accommodation.insert()

        return review_pb2.Empty()
