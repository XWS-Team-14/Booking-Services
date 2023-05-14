import grpc
import json

from proto import accommodation_crud_pb2, accommodation_crud_pb2_grpc
from proto import search_pb2_grpc, search_pb2
from proto import availability_crud_pb2, availability_crud_pb2_grpc

from google.protobuf.json_format import MessageToJson

from app.config import get_yaml_config
from loguru import logger
from types import SimpleNamespace


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

        res = json.loads(
            MessageToJson(accs), object_hook=lambda d: SimpleNamespace(**d)
        )
        res2 = json.loads(
            MessageToJson(avvs), object_hook=lambda d: SimpleNamespace(**d)
        )

        # fix paths for image_urls
        result = search_pb2.SearchResults()
        try:
            logger.info(res)
            for item in res.items:
                logger.info(res2)
                for item2 in res2.items:
                    if item.id == item2.accomodationId:
                        location = search_pb2.Location(
                            country=item.location.country,
                            city=item.location.city,
                            address=item.location.address,
                        )
                        features_list = list()
                        image_urls_list = list()

                        for features in item.features:
                            features_list.append(features)
                        for urls in item.imageUrls:
                            image_urls_list.append(urls)

                        amongas = search_pb2.SearchResult(
                            accommodation_id=item.id,
                            host_id=item.userId,
                            name=item.name,
                            location=location,
                            features=features_list,
                            image_urls=image_urls_list,
                            min_guests=item.minGuests,
                            max_guests=item.maxGuests,
                            base_price=item2.basePrice,
                            total_price=item2.totalPrice,
                            auto_accept_flag=item.autoAcceptFlag,
                        )

                        result.items.append(amongas)
        except Exception as e:
            logger.error(f"Error {e}")

        return result
