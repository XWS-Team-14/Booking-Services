import json
from typing import Annotated

import grpc
from fastapi import APIRouter, Cookie
from fastapi_utils.cbv import cbv
import httpx
from google.protobuf.json_format import MessageToJson
import urllib.parse

from app.utils.jwt import get_role_from_token, get_id_from_token
from proto import notification_pb2_grpc, notification_pb2
from starlette.responses import HTMLResponse, Response

from app import schemas
from app.constants import notification_server, airline_server
from app.utils import get_server
from opentelemetry.instrumentation.grpc import aio_client_interceptors
from jwt import ExpiredSignatureError, InvalidTokenError

router = APIRouter()


@cbv(router)
class Flights:
    @router.get("/", response_class=HTMLResponse,
                description="Get suggested flights")
    async def getSuggestedFlights(self,
                                  start_date: str,
                                  end_date: str,
                                  start_country: str,
                                  end_country: str,
                                  start_city: str,
                                  end_city: str,
                                  count: int):
        params_start = {
            'date': start_date,
            'start_country': start_country,
            'start_city': start_city,
            'end_country': end_country,
            'end_city': end_city,
            'space_needed': count
        }

        params_end = {
            'date': end_date,
            'start_country': end_country,
            'start_city': end_city,
            'end_country': start_country,
            'end_city': start_city,
            'space_needed': count
        }

        path = f"{airline_server}/api/search-external/"
        response_outbound = httpx.get(path, params=params_start)
        response_inbound = httpx.get(path, params=params_end)
        content = {
            'outbound': response_outbound.json()['results'],
            'inbound': response_inbound.json()['results']
        }
        data = json.dumps(content)
        return Response(status_code=200, media_type="application/json", content=data)
