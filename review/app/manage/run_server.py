import asyncio

from loguru import logger
import grpc

from app.core import listen_to_reservations
from app.core.review_servicer import ReviewServicer
from app.db.mongodb import start_async_mongodb
from proto import review_pb2_grpc, review_pb2
from app.core import listen_to_reservations

# Telemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.grpc import aio_server_interceptor
from app.core.data_migrator import start_data_migrator

resource = Resource(attributes={
    SERVICE_NAME: "review"
})

provider = TracerProvider(resource=resource)
jaeger_exporter = JaegerExporter(
    agent_host_name='jaeger',
    agent_port=6831,
)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

_cleanup_coroutines = []

async def serve(port):
    server = grpc.aio.server(interceptors = [aio_server_interceptor()])
    # Add services
    review_pb2_grpc.add_ReviewServiceServicer_to_server(ReviewServicer(), server)
    server.add_insecure_port('[::]:' + port)
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

    asyncio.create_task(start_data_migrator())
    _cleanup_coroutines.append(server_graceful_shutdown())
    asyncio.create_task(listen_to_reservations())

    await server.wait_for_termination()
