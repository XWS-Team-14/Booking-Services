from proto import review_pb2_grpc, review_pb2

from app.core.review_helper import ReviewHelper


class ReviewServicer(review_pb2_grpc.ReviewServiceServicer):
    async def Test(self, request, context):
        ReviewHelper.listen_to_reservations()
