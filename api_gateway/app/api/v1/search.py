import json
from typing import Annotated, Union

import grpc

from app.constants import search_server
from app.schemas.search import DateInterval, Location, SearchParams, SearchResults
from app.utils.get_server import get_server
from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse
from google.protobuf.json_format import MessageToDict, Parse
from loguru import logger

from proto import search_pb2, search_pb2_grpc
from opentelemetry.instrumentation.grpc import aio_client_interceptors

router = APIRouter(
    tags=["Search"],
)


@router.get(
    "/",
    description="Search",
)
async def search(
    country: str | None = "",
    city: str | None = "",
    address: str | None = "",
    guests: int | None = 0,
    date_start: str | None = "",
    date_end: str | None = "",
    price_min: int | None = 0,
    price_max: int | None = None,
    amenities: Annotated[Union[list[str], None], Query()] = None,
    must_be_featured_host: bool | None = False
):
    print(amenities)
    amenities = [] if amenities is None else amenities
    price_max = -1 if price_max is None else price_max
    params = SearchParams(
        location=Location(country=country, city=city, address=address),
        guests=guests,
        interval=DateInterval(date_start=date_start, date_end=date_end),
        amenities=amenities,
        price_min=price_min,
        price_max=price_max,
        must_be_featured_host=must_be_featured_host
    )
    async with grpc.aio.insecure_channel(search_server, interceptors=aio_client_interceptors()) as channel:
        stub = search_pb2_grpc.SearchStub(channel)
        data = await stub.Search(
            Parse(json.dumps(params.dict()), search_pb2.SearchParams())
        )
    res = SearchResults.parse_obj(MessageToDict(data, preserving_proto_field_name=True))
    # fix paths for image_urls
    updated_url = "http://localhost:8888/api/static/images/"
    try:
        for item in res.items:
            updated_urls = []
            for img_url in item.image_urls:
                updated_urls.append(updated_url + img_url)
            item.image_urls = updated_urls
    except Exception as e:
        logger.error(f"Error {e}")
    return ORJSONResponse(status_code=res.response.status_code, content=res.dict())
