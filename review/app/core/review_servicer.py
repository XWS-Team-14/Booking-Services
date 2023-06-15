import uuid

from loguru import logger
from proto import review_pb2_grpc, review_pb2

from app.models.accommodation import Accommodation
from app.models.host import Host


class ReviewServicer(review_pb2_grpc.ReviewServiceServicer):
    async def GetHostStatus(self, request, context):
        logger.info(f'Fetching host {request.id} status')
        host = await Host.get(uuid.UUID(request.id))

        if host is None:
            return review_pb2.HostStatus(error_message="Host not found", error_code=404)
        else:
            return review_pb2.HostStatus(id=request.id, status=host.is_featured())

    async def GetAllAccommodationsWithFeaturedHost(self, request, context):
        all_accommodations = await Accommodation.find_all()
        featured_accommodations = []
        for accommodation in all_accommodations:
            if accommodation.host.is_featured():
                featured_accommodations.append(accommodation)

        return review_pb2.Accommodations(accommodation_id=featured_accommodations)

