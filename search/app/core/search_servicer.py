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
        print('1')
        parsed_request = SearchParams.parse_obj(
            MessageToDict(request, preserving_proto_field_name=True)
        )
        print('2')

        async with grpc.aio.insecure_channel(accommodation_server, interceptors=aio_client_interceptors()) as channel:
            stub = accommodation_pb2_grpc.AccommodationServiceStub(channel)
            data = Parse(
                json.dumps(parsed_request.dict(exclude={"interval", "price_min", "price_max", "must_be_featured_host"}), cls=UUIDEncoder),
                accommodation_pb2.SearchParams(),
            )
            accs = await stub.GetBySearch(data)
        print('3')
        async with grpc.aio.insecure_channel(availability_server, interceptors=aio_client_interceptors()) as channel:
            stub2 = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
            data = Parse(
                json.dumps(parsed_request.dict(exclude={"location", "amenities", "must_be_featured_host"}), cls=UUIDEncoder),
                availability_crud_pb2.SearchDetails(),
            )
            avvs = await stub2.GetAllSearch(data)
        print('4')
        print('5')

        parsed_accs = ResponseAccommodations.parse_obj(
            MessageToDict(accs, preserving_proto_field_name=True)
        )

        parsed_avvs = ExpandedAvailabilityDtos.parse_obj(
            MessageToDict(avvs, preserving_proto_field_name=True)
        )

        if parsed_request.must_be_featured_host:
            async with grpc.aio.insecure_channel(review_server) as channel:
                stub_review = review_pb2_grpc.ReviewServiceStub(channel)
                grpc_review_response = MessageToDict(await stub_review.GetAllAccommodationsWithFeaturedHost(review_pb2.Empty()))
                if grpc_review_response.error_message:
                    logger.info(f"{grpc_review_response.error_code}: {grpc_review_response.error_message}")

        result = SearchResults.construct()

        if parsed_accs.response.status_code != 200:
            result.response.status_code = parsed_accs.response.status_code
            result.response.message_string = parsed_accs.response.message_string
            return Parse(
                json.dumps(result.dict(), cls=UUIDEncoder), search_pb2.SearchResults()
            )

        acc_dct = {parsed_accs.items[i].id: parsed_accs.items[i] for i in range(0, len(parsed_accs.items))}
        avv_dct = {parsed_avvs.items[i].accommodation_id: parsed_avvs.items[i] for i in range(0, len(parsed_avvs.items))}
        # if parsed_avvs.response.status_code != 200:
        #    result.response.status_code = parsed_avvs.response.status_code
        #    result.response.message_string = parsed_avvs.response.message_string
        #    return Parse(
        #        json.dumps(result.dict(), cls=UUIDEncoder), search_pb2.SearchResults()
        #    )
        for item_id in acc_dct:
            item = acc_dct[item_id]
            availability = avv_dct[item_id]
            amenities = item.features
            price = availability.total_price
            can_be_added = True
            for amenity in parsed_request.amenities:
                if amenity not in amenities:
                    can_be_added = False
                    break

            if not (parsed_request.price_min <= price <= parsed_request.price_max):
                can_be_added = False

            if parsed_request.must_be_featured_host:


            if can_be_added:
                result.items.append(SearchResult.construct().create(item, availability))
        else:
            result.response.message_string = "Success!"
            result.response.status_code = 200
            logger.info(result)
            logger.success("Fetched search data")
        return Parse(
            json.dumps(result.dict(), cls=UUIDEncoder), search_pb2.SearchResults()
        )
