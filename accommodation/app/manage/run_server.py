from loguru import logger
from app.core.accommodation_servicer import AccommodationServicer
from app.db.mongodb import start_async_mongodb
from proto import accommodation_pb2_grpc
import grpc
import asyncio
from app.core.orchestrator_listener import listen_to_delete_messages

# Telemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.grpc import aio_server_interceptor

resource = Resource(attributes={
    SERVICE_NAME: "accommodation"
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
    accommodation_pb2_grpc.add_AccommodationServiceServicer_to_server(
        AccommodationServicer(), server
    )

    server.add_insecure_port("[::]:" + port)
    logger.info("Connecting to the database")
    await start_async_mongodb()
    logger.info("Starting GRPC server")
    await server.start()
    logger.success(f"GRPC server has started on port {port}, waiting for termination")

    async def server_graceful_shutdown(*_):
        logger.info("Starting graceful shutdown...")
        # Shuts down the server with 5 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())

    asyncio.create_task(listen_to_delete_messages())
    await server.wait_for_termination()
