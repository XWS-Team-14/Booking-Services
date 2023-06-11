import uuid

from loguru import logger
from proto import review_pb2_grpc, review_pb2

from app.models.host import Host


class ReviewServicer(review_pb2_grpc.ReviewServiceServicer):
    async def GetHostStatus(self, request, context):
        logger.info(f'Fetching host {request.id} status')
        host = await Host.get(uuid.UUID(request.id))

        if host is None:
            return review_pb2.HostStatus(error_message="Host not found", error_code=404)
        else:
            return review_pb2.HostStatus(id=request.id, status=host.is_featured())
