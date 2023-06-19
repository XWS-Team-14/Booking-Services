import asyncio
import json
from typing import Annotated

import grpc
from fastapi import APIRouter, status, Cookie
from fastapi.responses import Response
import uuid

from starlette.websockets import WebSocket
from aiokafka import AIOKafkaConsumer
from websockets.exceptions import ConnectionClosedError

from proto import orchestrator_pb2, orchestrator_pb2_grpc
from ...constants import orchestrator_server, kafka_server
from loguru import logger
from opentelemetry.instrumentation.grpc import aio_client_interceptors
from jwt import ExpiredSignatureError, InvalidTokenError

from ...utils.jwt import get_role_from_token, get_id_from_token

router = APIRouter(tags=["Orchestrator"], )


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT, description="Delete User via SAGA", )
async def deleteUser(access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing delete user via saga request")
    async with grpc.aio.insecure_channel(orchestrator_server, interceptors=aio_client_interceptors()) as channel:
        try:
            user_id = get_id_from_token(access_token)
            user_role = get_role_from_token(access_token)
        except ExpiredSignatureError:
            return Response(status_code=401, media_type="text/html", content="Token expired.")
        except InvalidTokenError:
            return Response(status_code=401, media_type="text/html", content="Invalid token.")
        stub = orchestrator_pb2_grpc.OrchestratorStub(channel)
        data = await stub.DeleteUser(orchestrator_pb2.UserId(id=user_id))
        logger.info(data)
        logger.info(data.error_message)
        logger.info(data.error_code)
    return Response(status_code=data.error_code, media_type="text/html", content=data.error_message)


@router.websocket("/status")
async def websocket_delete_update(websocket: WebSocket):
    await websocket.accept()
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer("delete-status-update", loop=loop, bootstrap_servers=kafka_server,
                                value_deserializer=lambda m: json.loads(m.decode('ascii')))

    await consumer.start()

    while True:
        try:
            async for msg in consumer:
                message = msg.value
                status = message['status']
                print(msg)
                print(status)
                await websocket.send_text(f'Status: {str(status)}')
                break
        except ConnectionClosedError:
            print("Client disconnected.")
            break
        finally:
            await consumer.stop()
