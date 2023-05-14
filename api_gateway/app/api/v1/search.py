import json
import grpc
from app.config import get_yaml_config
from fastapi import APIRouter
from fastapi.responses import Response
from proto import search_pb2_grpc, search_pb2
from loguru import logger
from types import SimpleNamespace
from google.protobuf.json_format import MessageToJson

router = APIRouter(
    tags=["Search"],
)


@router.post(
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
    search_server = (
        get_yaml_config().get("search_server").get("ip")
        + ":"
        + get_yaml_config().get("search_server").get("port")
    )
    location = search_pb2.Location(
        city=city,
        country=country,
        address=address,
    )
    interval = search_pb2.Interval(date_start=date_start, date_end=date_end)
    request_data = search_pb2.SearchParams(
        location=location, details=interval, guests=guests
    )
    async with grpc.aio.insecure_channel(search_server) as channel:
        stub = search_pb2_grpc.SearchStub(channel)
        data = await stub.Search(request_data)
        res = json.loads(
            MessageToJson(data), object_hook=lambda d: SimpleNamespace(**d)
        )
        # fix paths for image_urls
        updated_url = "http://localhost:8000/api/static/images/"
        try:
            for item in res.items:
                updated_urls = []
                for img_url in item.imageUrls:
                    updated_urls.append(updated_url + img_url)
                item.imageUrls = updated_urls
        except Exception as e:
            logger.error(f"Error {e}")

    return Response(status_code=200, media_type="application/json", content=res)
