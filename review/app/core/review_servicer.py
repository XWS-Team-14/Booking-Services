from proto import review_pb2_grpc, review_pb2


class ReviewServicer(review_pb2_grpc.ReviewServiceServicer):
    async def Test(self, request, context):
        raise NotImplementedError
