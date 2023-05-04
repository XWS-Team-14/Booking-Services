
from app.models.accommodation import Accommodation
from proto import accommodation_crud_pb2_grpc, accommodation_crud_pb2
from loguru import logger


class AccommodationServicer(accommodation_crud_pb2_grpc.AccommodationCrudServicer):

    async def Delete(self, request, context):
        logger.info('Delete request started')
        # compute data and stuff
        obj_to_delete = await Accommodation.find_one(id == request.id)
        if obj_to_delete is None:
            logger.error('Trying to delete object that does not exist')
        else:
            await obj_to_delete.delete()
            logger.success(f'Deleted an object with id = {request.id}')
        return accommodation_crud_pb2.Empty()
