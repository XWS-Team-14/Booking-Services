import os
from concurrent import futures
from proto import accommodation_crud_pb2_grpc
import grpc

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accommodation.settings')
from service.views import AccommodationServicer



def serve(port):

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add services
    accommodation_crud_pb2_grpc.add_AccommodationCrudServicer_to_server(AccommodationServicer(), server)

    server.add_insecure_port('[::]:'+port)
    server.start()
    print('Server has started, waiting for termination')
    server.wait_for_termination()
