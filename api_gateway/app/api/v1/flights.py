import json
from typing import Annotated, Union

import httpx
from fastapi import APIRouter, Header
from fastapi_utils.cbv import cbv
from starlette.responses import HTMLResponse, Response

from app import schemas
from app.constants import airline_server

router = APIRouter()


@cbv(router)
class Flights:
    @router.get("/", response_class=HTMLResponse, description="Get suggested flights")
    async def get_suggested_flights(self, start_date: str, end_date: str, start_country: str, end_country: str,
                                    start_city: str, end_city: str, count: int):
        params_start = {'date': start_date, 'start_country': start_country, 'start_city': start_city,
            'end_country': end_country, 'end_city': end_city, 'space_needed': count}

        params_end = {'date': end_date, 'start_country': end_country, 'start_city': end_city,
            'end_country': start_country, 'end_city': start_city, 'space_needed': count}

        path = f"{airline_server}/api/search-external/"
        response_outbound = httpx.get(path, params=params_start)
        response_inbound = httpx.get(path, params=params_end)
        content = {'outbound': response_outbound.json()['results'], 'inbound': response_inbound.json()['results']}
        data = json.dumps(content)
        return Response(status_code=200, media_type="application/json", content=data)

    @router.post("/purchase", response_class=HTMLResponse, description="Purchase ticket")
    async def purchase(self, payload: schemas.TicketPurchase,
                       http_api_key: Annotated[Union[str, None], Header(convert_underscores=False)] = None):
        path = f"{airline_server}/api/key/purchase"
        data = json.dumps(payload.__dict__)
        with httpx.Client() as client:
            headers = {'HTTP_API_KEY': http_api_key}
            response = client.post(path, json=data, headers=headers)
            print(response)
