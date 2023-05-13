import uuid

from proto import accommodation_crud_pb2_grpc, accommodation_crud_pb2
from loguru import logger
from ..models.test import Question


class AccommodationServicer(accommodation_crud_pb2_grpc.AccommodationCrudServicer):
    async def Search(self, request, context):
        logger.success("Request handled")
        # compute data and stuff
        a = Question(
            title="test", credit=15, question_id=uuid.uuid4(), contest_name="test2"
        )
        await a.insert()
        return accommodation_crud_pb2.Empty()
