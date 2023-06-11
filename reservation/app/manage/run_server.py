from loguru import logger

from proto import reservation_crud_pb2_grpc
import grpc

from ..core.reservation_servicer import ReservationServicer
from ..db.mongodb import start_async_mongodb


_cleanup_coroutines = []


async def serve(port):
    server = grpc.aio.server()
    # Add services
    reservation_crud_pb2_grpc.add_ReservationCrudServicer_to_server(ReservationServicer(), server)

    server.add_insecure_port('[::]:'+port)
    logger.info('Connecting to the database')
    await start_async_mongodb()
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
