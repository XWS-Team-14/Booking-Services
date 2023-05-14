import grpc

from proto import accommodation_crud_pb2, accommodation_crud_pb2_grpc
from proto import search_pb2_grpc, search_pb2
from proto import availability_crud_pb2, availability_crud_pb2_grpc

from app.config import get_yaml_config
from loguru import logger


class SearchServicer(search_pb2_grpc.SearchServicer):
    async def Search(self, request, context):
        availability_server = (
            get_yaml_config().get("availability_server").get("ip")
            + ":"
            + get_yaml_config().get("availability_server").get("port")
        )

        accommodation_server = (
            get_yaml_config().get("accommodation_server").get("ip")
            + ":"
            + get_yaml_config().get("accommodation_server").get("port")
        )

        logger.info("1")
        logger.info(request)
        async with grpc.aio.insecure_channel(accommodation_server) as channel:
            logger.info("2")
            stub = accommodation_crud_pb2_grpc.AccommodationCrudStub(channel)
            logger.info("5")
            location = accommodation_crud_pb2.Location(
                country=request.location.country,
                city=request.location.city,
                address=request.location.address,
            )
            data = accommodation_crud_pb2.SearchParamsAcc(
                location=location, guests=request.guests
            )
            logger.info("3")
            logger.info(data)
            accs = await stub.GetBySearch(data)
        logger.info(accs)
        async with grpc.aio.insecure_channel(availability_server) as channel:
            stub2 = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)

            interval = availability_crud_pb2.Interval(
                date_start=request.details.date_start,
                date_end=request.details.date_end,
            )

            params = availability_crud_pb2.SearchDetails(
                interval=interval, num_of_guests=request.guests
            )
            avvs = await stub2.GetAllSearch(params)
        logger.info(avvs)
        return search_pb2.SearchResults()
