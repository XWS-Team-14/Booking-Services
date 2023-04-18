import os
from concurrent import futures

import grpc


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add services

    server.add_insecure_port('[::]:'+port)
    server.start()
    print('Server has started, waiting for termination')
    server.wait_for_termination()
