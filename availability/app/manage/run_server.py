from app.manage.init_holidays import init_holidays
from loguru import logger
from app.core.availability_servicer import AvailabilityServicer
from app.db.mongodb import start_async_mongodb
from proto import availability_crud_pb2_grpc
import grpc
import asyncio
from app.core.orchestrator_listener import listen_to_delete_messages
_cleanup_coroutines = []


async def serve(port):
    server = grpc.aio.server()
    # Add services
    availability_crud_pb2_grpc.add_AvailabilityCrudServicer_to_server(AvailabilityServicer(), server)

    server.add_insecure_port('[::]:'+port)
    logger.info('Connecting to the database')
    await start_async_mongodb()
    logger.info('Starting GRPC server')
    await server.start()
    #await init_holidays();
    logger.success(f'GRPC server has started on port {port}, waiting for termination')
    async def server_graceful_shutdown(*_):
        logger.info("Starting graceful shutdown...")
        # Shuts down the server with 5 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    
    asyncio.create_task(listen_to_delete_messages())
    await server.wait_for_termination()
