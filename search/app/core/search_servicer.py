import grpc
import json

from proto import accommodation_pb2, accommodation_pb2_grpc
from proto import search_pb2, search_pb2_grpc
from proto import availability_crud_pb2, availability_crud_pb2_grpc

from google.protobuf.json_format import MessageToDict, Parse

from loguru import logger
from app.utils.json_encoder import UUIDEncoder
from app.utils.get_server import get_server
from app.models.protobuf_models import (
    SearchParams,
    ResponseAccommodations,
    ExpandedAvailabilityDtos,
)
from app.models.export_results import SearchResults, SearchResult


class SearchServicer(search_pb2_grpc.SearchServicer):
    async def Search(self, request, context):
        availability_server = get_server("availability_server")
        accommodation_server = get_server("accommodation_server")

        parsed_request = SearchParams.parse_obj(
            MessageToDict(request, preserving_proto_field_name=True)
        )

        async with grpc.aio.insecure_channel(accommodation_server) as channel:
            stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)
            data = Parse(
                json.dumps(parsed_request.dict(exclude={"interval"}), cls=UUIDEncoder),
                accommodation_pb2.SearchParams(),
            )
            accs = await stub.GetBySearch(data)

        async with grpc.aio.insecure_channel(availability_server) as channel:
            stub2 = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
            data = Parse(
                json.dumps(parsed_request.dict(exclude={"location"}), cls=UUIDEncoder),
                availability_crud_pb2.SearchDetails(),
            )
            avvs = await stub2.GetAllSearch(data)

        parsed_accs = ResponseAccommodations.parse_obj(
            MessageToDict(accs, preserving_proto_field_name=True)
        )

        parsed_avvs = ExpandedAvailabilityDtos.parse_obj(
            MessageToDict(avvs, preserving_proto_field_name=True)
        )

        result = SearchResults.construct()
        try:
            for item in parsed_accs.items:
                for item2 in parsed_avvs.items:
                    if item.id == item2.accommodation_id:
                        result.items.append(
                            SearchResult.construct().create(item, item2)
                        )
                        break
        except Exception as e:
            logger.error(f"Error {e}")
            result.response.message_string = e
            result.response.status_code = 500
        else:
            result.response.message_string = "Success!"
            result.response.status_code = 200
            logger.info(result)
            logger.success("Fetched search data")
        return Parse(
            json.dumps(result.dict(), cls=UUIDEncoder), search_pb2.SearchResults()
        )
