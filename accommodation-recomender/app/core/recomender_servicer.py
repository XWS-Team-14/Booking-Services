import uuid

from proto import accommodation_recomender_pb2_grpc, accommodation_recomender_pb2
from loguru import logger



class RecomenderServicer(accommodation_recomender_pb2_grpc.AccommodationRecomenderServicer):

    async def GetRecomended(self, request, context):
        logger.success(f'Fetch recommended for user {request.id} request recieved')
        # compute data and stuff
        return accommodation_recomender_pb2.Accommodation_ids()
