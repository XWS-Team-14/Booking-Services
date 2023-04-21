import time
import uuid

from proto import accommodation_crud_pb2_grpc, accommodation_crud_pb2
from .models import Question


class AccommodationServicer(accommodation_crud_pb2_grpc.AccommodationCrudServicer):

    def Delete(self, request, context):
        # compute data and stuff
        time.sleep(5)
        a = Question(title='test', credit="15", id=uuid.uuid4(), contest_name='test2')
        a.save()
        return accommodation_crud_pb2.Empty()
