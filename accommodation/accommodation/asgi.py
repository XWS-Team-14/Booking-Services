import os
from concurrent import futures

import grpc
from service.views import TestGreeter

from proto import test_pb2_grpc

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add services
    test_pb2_grpc.add_GreeterServicer_to_server(TestGreeter(), server)

    server.add_insecure_port('[::]:'+port)
    server.start()
    print('Server has started, waiting for termination')
    server.wait_for_termination()
