import asyncio

from loguru import logger
import grpc

from app.core import listen_to_reservations
from app.core.review_servicer import ReviewServicer

_cleanup_coroutines = []
from proto import review_pb2_grpc, review_pb2
from app.core import listen_to_reservations


async def serve(port):
    server = grpc.aio.server()
    # Add services
    review_pb2_grpc.add_ReviewServiceServicer_to_server(ReviewServicer(), server)
    server.add_insecure_port('[::]:' + port)
    logger.info('Starting GRPC server')
    await server.start()
    logger.success(f'GRPC server has started on port {port}, waiting for termination')

    async def server_graceful_shutdown(*_):
        logger.info("Starting graceful shutdown...")
        # Shuts down the server with 5 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())

    await server.wait_for_termination()
