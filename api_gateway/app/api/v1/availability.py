from ...schemas.availability import AvailabilityDto
from ...config import get_yaml_config
from fastapi import APIRouter, status, Cookie
from fastapi.responses import Response

# from fastapi_utils.cbv import cbv
from google.protobuf import json_format
from typing import Annotated
from loguru import logger
import grpc
from proto import availability_crud_pb2_grpc, availability_crud_pb2
from proto import accommodation_pb2_grpc, accommodation_pb2
from ...utils.jwt import get_role_from_token, get_id_from_token
from jwt import ExpiredSignatureError, InvalidTokenError

router = APIRouter(
    tags=["Availability"],
)


@router.get(
    "/all",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all availabilities",
)
async def getAll():
    logger.info("Gateway processing getAll Availability request")
    availability_server = (
        get_yaml_config().get("availability_server").get("ip")
        + ":"
        + get_yaml_config().get("availability_server").get("port")
    )
    async with grpc.aio.insecure_channel(availability_server) as channel:
        stub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
        logger.info("Gateway processing getAll Availability data")
        data = await stub.GetAll({})
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(status_code=200, media_type="application/json", content=json)


@router.get(
    "/id/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get one availability by id",
)
async def getById(item_id):
    logger.info("Gateway processing getById Availability request")
    availability_server = (
        get_yaml_config().get("availability_server").get("ip")
        + ":"
        + get_yaml_config().get("availability_server").get("port")
    )
    async with grpc.aio.insecure_channel(availability_server) as channel:
        stub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
        data = await stub.GetById(availability_crud_pb2.AvailabilityId(id=item_id))
        if data.availability_id == "":
            return Response(
                status_code=200, media_type="application/json", content="Invalid id"
            )
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(status_code=200, media_type="application/json", content=json)


@router.get(
    "/user/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get one availability by id",
)
async def getForUser(access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing getByUser Availability request")
    try:
        user_id = get_id_from_token(access_token)
        user_role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if user_role != "host":
        return Response(status_code=401, media_type="text/html", content="Unauthorized")

    accommodation_server = (
        get_yaml_config().get("accommodation_server").get("ip")
        + ":"
        + get_yaml_config().get("accommodation_server").get("port")
    )

    availability_server = (
        get_yaml_config().get("availability_server").get("ip")
        + ":"
        + get_yaml_config().get("availability_server").get("port")
    )

    async with grpc.aio.insecure_channel(availability_server) as channel:
        stub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
        availability_data = await stub.GetAll({})
    logger.info("Gateway fetched Availability data")
    async with grpc.aio.insecure_channel(accommodation_server) as channel:
        stub = accommodation_pb2_grpc.AccommodationCrudStub(channel)
        dto = accommodation_pb2.InputId(
            id=user_id,
        )
        accommodation_data = await stub.GetByUser(dto)
    logger.info("Gateway fetched Accommodation data")
    retVal = availability_crud_pb2.AvailabilityDtos()
    if accommodation_data:
        for item in availability_data.items:
            if any(item.accomodation_id == x.id for x in accommodation_data.items):
                retVal.items.append(item)

    json = json_format.MessageToJson(retVal, preserving_proto_field_name=True)
    return Response(status_code=200, media_type="application/json", content=json)


@router.get(
    "/accommodation/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get one availability by id",
)
async def getByAccommodation(
    item_id, access_token: Annotated[str | None, Cookie()] = None
):
    logger.info("Gateway processing getByUser Availability request")
    try:
        get_id_from_token(access_token)
        get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    availability_server = (
        get_yaml_config().get("availability_server").get("ip")
        + ":"
        + get_yaml_config().get("availability_server").get("port")
    )

    async with grpc.aio.insecure_channel(availability_server) as channel:
        stub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
        availability_data = await stub.GetByAccommodationId(
            availability_crud_pb2.AvailabilityId(id=item_id)
        )
    logger.info("Gateway fetched Availability data")

    json = json_format.MessageToJson(
        availability_data, preserving_proto_field_name=True
    )
    return Response(status_code=200, media_type="application/json", content=json)


@router.post(
    "/create",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Create new availability",
)
async def create(
    item: AvailabilityDto, access_token: Annotated[str | None, Cookie()] = None
):
    logger.info("Gateway processing create Availability request")
    try:
        role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if role != "host":
        return Response(status_code=401, media_type="text/html", content="Invalid role")
    availability_server = (
        get_yaml_config().get("availability_server").get("ip")
        + ":"
        + get_yaml_config().get("availability_server").get("port")
    )
    async with grpc.aio.insecure_channel(availability_server) as channel:
        stub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)

        availability = availability_crud_pb2.AvailabilityDto()
        availability.availability_id = item.availability_id
        availability.accomodation_id = item.accomodation_id
        availability.interval.date_start = item.interval.date_start
        availability.interval.date_end = item.interval.date_end
        availability.base_price = item.base_price
        availability.pricing_type = item.pricing_type
        for pricing in item.special_pricing:
            availability.special_pricing.append(
                availability_crud_pb2.SpecialPricing(
                    title=pricing.title, pricing_markup=pricing.pricing_markup
                )
            )

        response = await stub.Create(availability)
        if response.status == "Invalid date":
            return Response(
                status_code=200, media_type="application/json", content="Invalid date"
            )
    return Response(status_code=200, media_type="application/json", content="Success")


@router.put(
    "/update",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update availability",
)
async def update(
    item: AvailabilityDto, access_token: Annotated[str | None, Cookie()] = None
):
    logger.info("Gateway processing update Availability request")
    try:
        role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if role != "host":
        return Response(status_code=401, media_type="text/html", content="Invalid role")
    availability_server = (
        get_yaml_config().get("availability_server").get("ip")
        + ":"
        + get_yaml_config().get("availability_server").get("port")
    )
    async with grpc.aio.insecure_channel(availability_server) as channel:
        stub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)

        availability = availability_crud_pb2.AvailabilityDto()
        availability.availability_id = item.availability_id
        availability.accomodation_id = item.accomodation_id
        availability.interval.date_start = item.interval.date_start
        availability.interval.date_end = item.interval.date_end
        availability.base_price = item.base_price
        availability.pricing_type = item.pricing_type
        for pricing in item.special_pricing:
            availability.special_pricing.append(
                availability_crud_pb2.SpecialPricing(
                    title=pricing.title, pricing_markup=pricing.pricing_markup
                )
            )

        response = await stub.Update(availability)
    return Response(
        status_code=200, media_type="application/json", content=response.status
    )


@router.delete(
    "/delete/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update availability",
)
async def delete(item_id, access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing delete Availability request")
    try:
        role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if role != "host":
        return Response(status_code=401, media_type="text/html", content="Invalid role")
    availability_server = (
        get_yaml_config().get("availability_server").get("ip")
        + ":"
        + get_yaml_config().get("availability_server").get("port")
    )
    async with grpc.aio.insecure_channel(availability_server) as channel:
        stub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
        data = await stub.Delete(availability_crud_pb2.AvailabilityId(id=item_id))
    return Response(status_code=200, media_type="application/json", content=data.status)
