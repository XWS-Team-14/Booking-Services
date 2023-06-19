from loguru import logger
from app.core.recomender_servicer import RecomenderServicer
from proto import accommodation_recomender_pb2_grpc
import grpc
from app.db.neomodel import start_neomodel
import asyncio
from app.core.migration_listener import listen_to_migrate_messages

# Telemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.grpc import aio_server_interceptor

resource = Resource(attributes={
    SERVICE_NAME: "accommodation-recommender"
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
    accommodation_recomender_pb2_grpc.add_AccommodationRecomenderServicer_to_server(RecomenderServicer(), server)

    server.add_insecure_port('[::]:'+port)
    logger.info('Starting GRPC server')
    await server.start()
    logger.success(f'GRPC server has started on port {port}, waiting for termination')

    async def server_graceful_shutdown(*_):
        logger.info("Starting graceful shutdown...")
        # Shuts down the server with 5 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)
    start_neomodel()
    asyncio.create_task(listen_to_migrate_messages())
    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()
