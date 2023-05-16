import uuid
from loguru import logger
from app.models.accommodation import Accommodation
from app.model.protobuf_models import (
    Response,
    InputId,
    ResponseAccommodation,
    ResponseAccommodations,
    SearchParams,
)
from proto import accommodation_pb2_grpc, accommodation_pb2
from google.protobuf.json_format import Parse, MessageToDict


class AccommodationServicer(accommodation_pb2_grpc.AccommodationServicer):
    async def Delete(self, request, context):
        logger.info("Delete request started")
        response = Response(message_string="", status_code=0)
        parsed_request = InputId.parse_obj(MessageToDict(request))
        try:
            await Accommodation.find_one(
                Accommodation.id == uuid.UUID(parsed_request.id)
            ).delete()
        except Exception as e:
            logger.error(f"Error {e}")
            response.message_string = e
            response.status_code = 500
        else:
            response.message_string = "Success!"
            response.status_code = 200
            logger.success(f"Deleted object with id = {parsed_request.id}")
        return Parse(response, accommodation_pb2.Response())

    async def DeleteByUser(self, request, context):
        logger.info("DeleteByUser request started")
        response = Response(message_string="", status_code=0)
        parsed_request = InputId.parse_obj(MessageToDict(request))
        try:
            await Accommodation.find(
                Accommodation.host_id == uuid.UUID(parsed_request.id)
            ).delete()
        except Exception as e:
            logger.error(f"Error {e}")
            response.message_string = e
            response.status_code = 500
        else:
            response.message_string = "Success!"
            response.status_code = 200
            logger.success(f"Deleted objects for user with id = {parsed_request.id}")
        return Parse(response, accommodation_pb2.Response())

    async def Create(self, request, context):
        logger.info("Create request started")
        response = Response(message_string="", status_code=0)
        parsed_request = Accommodation.parse_obj(MessageToDict(request))
        try:
            await parsed_request.insert()
        except Exception as e:
            logger.error(f"Error creating object {e}")
            response.message_string = e
            response.status_code = 500
        else:
            response.message_string = "Success!"
            response.status_code = 200
            logger.success(f"Created object with id = {request.id}")
        return Parse(response, accommodation_pb2.Response())

    async def Update(self, request, context):
        logger.info("Update request started")
        response = Response(message_string="", status_code=0)
        parsed_request = Accommodation.parse_obj(MessageToDict(request))
        try:
            await parsed_request.replace()
        except Exception as e:
            logger.error(f"Error updating object {e}")
            response.message_string = e
            response.status_code = 500
        else:
            response.message_string = "Success!"
            response.status_code = 200
            logger.success(f"Created object with id = {request.id}")
        return Parse(response, accommodation_pb2.Response())

    async def GetAll(self, request, context):
        logger.info("GetAll request started")
        response = ResponseAccommodations(response=Response(), items=[])
        try:
            response.items = await Accommodation.find().to_list()
        except Exception as e:
            logger.error(f"Error getting all objects {e}")
            response.response.message_string = e
            response.response.status_code = 500
        else:
            response.response.message_string = "Success!"
            response.response.status_code = 200
            logger.success("Sucessfully fetched all accommodations")
        return Parse(response, accommodation_pb2.ResponseAccommodations())

    async def GetById(self, request, context):
        logger.info("GetById request started")
        response = ResponseAccommodation(response=Response(), item=None)
        parsed_request = InputId.parse_obj(MessageToDict(request))
        try:
            response.item = await Accommodation.get(uuid.UUID(parsed_request.id))
        except Exception as e:
            logger.error(f"Error getting object {e}")
            response.response.message_string = e
            response.response.status_code = 500
        else:
            response.response.message_string = "Success!"
            response.response.status_code = 200
            logger.success("Sucessfully fetched all accommodations")
        return Parse(response, accommodation_pb2.ResponseAccommodation())

    async def GetBySearch(self, request, context):
        logger.info("GetBySearch request started")
        response = ResponseAccommodations(response=Response(), items=[])
        parsed_request = SearchParams.parse_obj(MessageToDict(request))
        try:
            response.items = await Accommodation.find_all().to_list()
            updated_list = []
            if parsed_request.location is not None:
                if (
                    parsed_request.location.city != ""
                    and parsed_request.location.city is not None
                ):
                    for item in response.items:
                        if item.location.city.find(parsed_request.location.city) != -1:
                            updated_list.append(item)
                    response.items = updated_list.copy()
                    updated_list = []
                if (
                    parsed_request.location.country != ""
                    and parsed_request.location.country is not None
                ):
                    for item in response.items:
                        if (
                            item.location.country.find(parsed_request.location.country)
                            != -1
                        ):
                            updated_list.append(item)
                    response.items = updated_list.copy()
                    updated_list = []
                if (
                    parsed_request.location.address != ""
                    and parsed_request.location.address is not None
                ):
                    for item in response.items:
                        if (
                            item.location.address.find(parsed_request.location.address)
                            != -1
                        ):
                            updated_list.append(item)
                    response.items = updated_list.copy()
                    updated_list = []
                if request.guests != 0 and request.guests is not None:
                    for item in response.items:
                        if (
                            item.min_guests <= request.guests
                            and item.max_guests >= request.guests
                        ):
                            updated_list.append(item)
                response.items = updated_list.copy()
        except Exception as e:
            logger.error(f"Error getting objects for search {e}")
            response.response.message_string = e
            response.response.status_code = 500
        else:
            response.response.message_string = "Success!"
            response.response.status_code = 200
            logger.success("Sucessfully fetched all accommodations for params")
        return Parse(response, accommodation_pb2.ResponseAccommodations())

    async def GetByUser(self, request, context):
        logger.info("GetByUser request started")
        response = ResponseAccommodations(response=Response(), items=[])
        parsed_request = InputId.parse_obj(MessageToDict(request))
        try:
            response.items = await Accommodation.find(
                Accommodation.host_id == uuid.UUID(parsed_request.id)
            ).to_list()
        except Exception as e:
            logger.error(f"Error getting objects for user {e}")
            response.response.message_string = e
            response.response.status_code = 500
        else:
            response.response.message_string = "Success!"
            response.response.status_code = 200
            logger.success(
                f"Sucessfully fetched all accommodations for user {parsed_request.id}"
            )
        return Parse(response, accommodation_pb2.ResponseAccommodations())
