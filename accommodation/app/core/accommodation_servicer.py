from app.models.accommodation import Accommodation
from proto import accommodation_crud_pb2_grpc, accommodation_crud_pb2
from loguru import logger


class AccommodationServicer(accommodation_crud_pb2_grpc.AccommodationCrudServicer):
    async def Delete(self, request, context):
        logger.info("Delete request started")
        # compute data and stuff
        try:
            obj_to_delete = await Accommodation.find_one(id == request.id)
        except Exception:
            logger.error("Trying to delete object that does not exist")
            return accommodation_crud_pb2.Empty()
        await obj_to_delete.delete()
        logger.success(f"Deleted an object with id = {request.id}")
        return accommodation_crud_pb2.Empty()
