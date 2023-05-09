import uuid
from availability.app.models.availability import Availability

from proto import availability_crud_pb2_grpc, availability_crud_pb2
from loguru import logger


class AvailabilityServicer(availability_crud_pb2_grpc.AvailabilityCrudServicer):
    """
    async def Delete(self, request, context):
        logger.success('Request handled')
        # compute data and stuff
        a = Question(title='test', credit=15, question_id=uuid.uuid4(), contest_name='test2')
        await a.insert()
        return accommodation_crud_pb2.Empty()
    """
    async def Create(self, request, context):
        logger.success('Request for creation Availability accepted');
        availability = Availability()
        await availability.insert()
        return availability_crud_pb2.Result("Success");