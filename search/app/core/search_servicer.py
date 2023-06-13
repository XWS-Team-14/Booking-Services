import json

import grpc
from app.models.export_results import SearchResult, SearchResults
from app.models.protobuf_models import (
    ExpandedAvailabilityDtos,
    ResponseAccommodations,
    SearchParams,
)
from app.utils.get_server import get_server
from app.utils.json_encoder import UUIDEncoder
from google.protobuf.json_format import MessageToDict, Parse
from loguru import logger

from proto import (
    accommodation_pb2,
    accommodation_pb2_grpc,
    availability_crud_pb2,
    availability_crud_pb2_grpc,
    search_pb2,
    search_pb2_grpc,
    review_pb2,
    review_pb2_grpc
)
from opentelemetry.instrumentation.grpc import aio_client_interceptors 

class SearchServicer(search_pb2_grpc.SearchServicer):
    async def Search(self, request, context):
        availability_server = get_server("availability_server")
        accommodation_server = get_server("accommodation_server")
        review_server = get_server("review_server")

        parsed_request = SearchParams.parse_obj(
            MessageToDict(request, preserving_proto_field_name=True)
        )

        async with grpc.aio.insecure_channel(accommodation_server, interceptors=aio_client_interceptors()) as channel:
            stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)
            data = Parse(
                json.dumps(parsed_request.dict(exclude={"interval"}), cls=UUIDEncoder),
                accommodation_pb2.SearchParams(),
            )
            accs = await stub.GetBySearch(data)

        async with grpc.aio.insecure_channel(availability_server, interceptors=aio_client_interceptors()) as channel:
            stub2 = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
            data = Parse(
                json.dumps(parsed_request.dict(exclude={"location"}), cls=UUIDEncoder),
                availability_crud_pb2.SearchDetails(),
            )
            avvs = await stub2.GetAllSearch(data)

        if parsed_request['must_be_featured_host']:
            async with grpc.aio.insecure_channel(review_server) as channel:
                stub_review = review_pb2_grpc.ReviewServiceStub(channel)
                grpc_review_response = await stub_review.GetAllAccommodationsWithFeaturedHost(review_pb2.Empty())
                if grpc_review_response.error_message:
                    logger.info(f"{grpc_review_response.error_code}: {grpc_review_response.error_message}")
                

        parsed_accs = ResponseAccommodations.parse_obj(
            MessageToDict(accs, preserving_proto_field_name=True)
        )

        parsed_avvs = ExpandedAvailabilityDtos.parse_obj(
            MessageToDict(avvs, preserving_proto_field_name=True)
        )

        result = SearchResults.construct()

        if parsed_accs.response.status_code != 200:
            result.response.status_code = parsed_accs.response.status_code
            result.response.message_string = parsed_accs.response.message_string
            return Parse(
                json.dumps(result.dict(), cls=UUIDEncoder), search_pb2.SearchResults()
            )
        # if parsed_avvs.response.status_code != 200:
        #    result.response.status_code = parsed_avvs.response.status_code
        #    result.response.message_string = parsed_avvs.response.message_string
        #    return Parse(
        #        json.dumps(result.dict(), cls=UUIDEncoder), search_pb2.SearchResults()
        #    )
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
