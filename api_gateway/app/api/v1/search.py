import json
import grpc
from fastapi import APIRouter
from proto import search_pb2_grpc, search_pb2
from loguru import logger
from google.protobuf.json_format import MessageToDict, Parse
from app.utils.get_server import get_server
from app.schemas.search import SearchParams, Location, DateInterval, SearchResults

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
):
    search_server = get_server("search_server")
    params = SearchParams(
        location=Location(country=country, city=city, address=address),
        guests=guests,
        interval=DateInterval(date_start=date_start, date_end=date_end),
    )
    async with grpc.aio.insecure_channel(search_server) as channel:
        stub = search_pb2_grpc.SearchStub(channel)
        data = await stub.Search(
            Parse(json.dumps(params.dict()), search_pb2.SearchParams())
        )
        res = SearchResults.parse_obj(
            MessageToDict(data, preserving_proto_field_name=True)
        )
        # fix paths for image_urls
        updated_url = "http://localhost:8000/api/static/images/"
        logger.info(res)
        try:
            for item in res.items:
                updated_urls = []
                for img_url in item.imageUrls:
                    updated_urls.append(updated_url + img_url)
                item.imageUrls = updated_urls
        except Exception as e:
            logger.error(f"Error {e}")
    return res.items
