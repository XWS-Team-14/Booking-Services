from loguru import logger
from app.core.accommodation_servicer import AccommodationServicer
from app.db.mongodb import start_async_mongodb
from proto import accommodation_crud_pb2_grpc
import grpc

_cleanup_coroutines = []


async def serve(port):
    server = grpc.aio.server()
    # Add services
    accommodation_crud_pb2_grpc.add_AccommodationCrudServicer_to_server(AccommodationServicer(), server)

    server.add_insecure_port('[::]:'+port)
    # Search probably doesn't need a database
    # logger.info('Connecting to the database')
    # await start_async_mongodb()
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
