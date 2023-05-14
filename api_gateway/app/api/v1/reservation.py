from typing import Annotated

from jwt import ExpiredSignatureError, InvalidTokenError

from ...schemas.reservation import ReservationDto, Guest
from ...config import get_yaml_config
from fastapi import APIRouter, status, Cookie
from fastapi.responses import Response
# from fastapi_utils.cbv import cbv
from google.protobuf import json_format
import json
from loguru import logger
import grpc
from proto import reservation_crud_pb2_grpc, reservation_crud_pb2, availability_crud_pb2_grpc, availability_crud_pb2
from ...utils.get_server import get_server
from ...utils.jwt import get_id_from_token, get_role_from_token

router = APIRouter(
    tags=["Reservation"],
)


@router.get(
    "/all",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all reservations",
)
async def getAll():
    logger.info("Gateway processing getAll reservations")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        logger.info("Gateway processing getAll reservation data")
        data = await stub.GetAll({})
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )

@router.get(
    "/all/guests",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all reservations",
)
async def getAllGuests():
    logger.info("Gateway processing getAll guests")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        logger.info("Gateway processing getAll reservation data")
        data = await stub.GetAllGuests({})
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )

@router.get(
    "/id/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get one reservation by id",
)
async def getById(item_id):
    logger.info("Gateway processing getById Reservation request")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.GetById(reservation_crud_pb2.ReservationId(id=item_id))
        if data.reservation_id == "":
            return Response(
                status_code=200, media_type="application/json", content="Invalid id"
            )
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )


@router.get(
    "/host}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all reservations by host id",
)
async def getByHost(access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing getPendingByHostId Reservation request")
    try:
        host_id = get_id_from_token(access_token)
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

    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.GetByHost(reservation_crud_pb2.HostId( id = host_id))
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )
@router.get(
    "/guest/id/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get one reservation by id",
)
async def getGuestById(item_id):
    logger.info("Gateway processing getGuestById  request")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.GetGuestById(reservation_crud_pb2.GuestId(id=item_id))
        if data.id == "":
            return Response(
                status_code=200, media_type="application/json", content="Invalid id"
            )
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )
@router.get(
    "/accommodation/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get one reservation by id",
)
async def getReservationsByAccommodation(item_id):
    logger.info("Gateway processing get reservations by accommodation  request")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.GetReservationsByAccommodation(reservation_crud_pb2.AccommodationResId(id=item_id))
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
        return Response(
            status_code=200, media_type="application/json", content=json
        )

@router.get(
    "/host/pending",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get pending reservations by host id",
)
async def getPendingByHost(access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing getPendingByHostId Reservation request")

    try:
        host_id = get_id_from_token(access_token)
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

    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.GetPendingReservationsByHost(reservation_crud_pb2.HostId(id = host_id))
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )

@router.get(
    "/host/active",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get pending reservations by host id",
)
async def getActiveByHost(access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing getPendingByHostId Reservation request")
    try:
        host_id = get_id_from_token(access_token)
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
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.GetActiveByHost(reservation_crud_pb2.HostId(id = host_id))
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )

@router.get(
    "/guest/active",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get pending reservations by guest id",
)
async def getActiveByGuest(access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing get active by guest Reservation request")
    try:
        guest_id = get_id_from_token(access_token)
        user_role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if user_role != "guest":
        return Response(status_code=401, media_type="text/html", content="Unauthorized")

    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.GetActiveByGuest(reservation_crud_pb2.GuestId(id = guest_id))
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )


@router.post(
    "/create",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Create new reservation",
)
async def create(item: ReservationDto):
    logger.info("Gateway processing create Availability request")
    availability_server = get_server("availability_server")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        reservation = reservation_crud_pb2.ReservationDto()
        reservation.reservation_id = str(item.reservation_id)
        reservation.accommodation.id = str(item.accommodation.id)
        reservation.accommodation.automaticAccept = item.accommodation.automaticAccept
        reservation.host_id = str(item.host_id)
        reservation.guest.id = str(item.guest.id)
        reservation.guest.canceledReservations = item.guest.canceledReservations
        reservation.number_of_guests = item.number_of_guests
        reservation.beginning_date = str(item.beginning_date)
        reservation.ending_date = str(item.ending_date)
        reservation.total_price = item.total_price
        if(reservation.accommodation.automaticAccept):
            async with grpc.aio.insecure_channel(availability_server) as channel:
                availabilityStub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
                reservation.status = 3
                availabilityStub.AddOccupiedInterval(availability_crud_pb2.UpdateIntervalDto(
                    id=availabilityStub.GetByAccommodationId(reservation.accommodation.id),
                    interval = availability_crud_pb2.Interval(
                        date_start = reservation.beginning_date,
                        end_date = reservation.ending_date) ))

        else:
            reservation.status = item.status

        response = await stub.Create(reservation)

        if response.status == "Invalid date":
            return Response(
                status_code=200, media_type="application/json", content="Invalid date"
            )

    return Response(
        status_code=200, media_type="application/json", content="Success"
    )

@router.post(
    "/create/guest",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Create new reservation",
)
async def createGuest(item: Guest):
    logger.info("Gateway processing create Availability request")

    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)

        guest = reservation_crud_pb2.Guest()
        guest.id = str(item.id)
        guest.canceledReservations = item.canceledReservations
        response = await stub.CreateGuest(guest)
    return Response(
        status_code=200, media_type="application/json", content="Success"
    )


@router.put(
    "/update",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update reservation",
)
async def update(item: ReservationDto):
    logger.info("Gateway processing update reservation request")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:

        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)

        reservation = reservation_crud_pb2.ReservationDto()
        reservation.reservation_id = str(item.reservation_id)
        reservation.accommodation.id = str(item.accommodation.id)
        reservation.accommodation.automaticAccept = item.accommodation.automaticAccept
        reservation.host_id = str(item.host_id)
        reservation.guest.id = str(item.guest.id)
        reservation.guest.canceledReservations = item.guest.canceledReservations
        reservation.number_of_guests = item.number_of_guests
        reservation.beginning_date = str(item.beginning_date)
        reservation.ending_date = str(item.ending_date)
        reservation.total_price = item.total_price
        reservation.status = item.status

        response = await stub.Update(reservation)
    return Response(
        status_code=200, media_type="application/json", content=response.status
    )

@router.put(
    "/update/guest",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update reservation",
)
async def updateGuest(item: Guest):
    logger.info("Gateway processing update reservation request")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:

        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)

        guest = reservation_crud_pb2.Guest()
        guest.id = str(item.id)
        guest.canceledReservations = item.canceledReservations

        response = await stub.UpdateGuest(guest)
    return Response(
        status_code=200, media_type="application/json", content=response.status
    )


@router.put(
    "/accept",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Accept a reservation",
)
async def AcceptReservation(item: ReservationDto, access_token: Annotated[str | None, Cookie()] = None):
    try:
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
    logger.info("Gateway processing accept reservation request")
    availability_server = get_server("availability_server")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:

        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)

        reservation = reservation_crud_pb2.ReservationDto()
        reservation.reservation_id = str(item.reservation_id)
        reservation.accommodation.id = str(item.accommodation.id)
        reservation.accommodation.automaticAccept = item.accommodation.automaticAccept
        reservation.host_id = str(item.host_id)
        reservation.guest.id = str(item.guest.id)
        reservation.guest.canceledReservations = item.guest.canceledReservations
        reservation.number_of_guests = item.number_of_guests
        reservation.beginning_date = str(item.beginning_date)
        reservation.ending_date = str(item.ending_date)
        reservation.total_price = item.total_price
        reservation.status = item.status

        response = await stub.AcceptReservation(reservation)

        async with grpc.aio.insecure_channel(availability_server) as channel:
            availabilityStub = availability_crud_pb2_grpc.AvailabilityCrudStub(channel)
            reservation.status = 3
            availabilityStub.AddOccupiedInterval(availability_crud_pb2.UpdateIntervalDto(
                id=availabilityStub.GetByAccommodationId(reservation.accommodation.id),
                interval=availability_crud_pb2.Interval(
                    date_start=reservation.beginning_date,
                    end_date=reservation.ending_date)))
        #after completing this step, adequate changes should be made in availability servicer

    return Response(
        status_code=200, media_type="application/json", content=response.status
    )

@router.delete(
    "/delete/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update reservation",
)
async def delete(item_id, access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing delete Reservation request")
    try:
        user_role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if user_role != "guest":
        return Response(status_code=401, media_type="text/html", content="Unauthorized")

    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.Delete(reservation_crud_pb2.ReservationId(id=item_id))
    return Response(
        status_code=200, media_type="application/json", content=data.status
    )

@router.delete(
    "/delete/guest/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update reservation",
)
async def deleteGuest(item_id):
    logger.info("Gateway processing delete guest request")
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.DeleteGuest(reservation_crud_pb2.Guest(id=item_id))
    return Response(
        status_code=200, media_type="application/json", content=data.status
    )