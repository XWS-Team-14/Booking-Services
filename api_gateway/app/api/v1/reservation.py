from ...schemas.reservation import ReservationDto
from ...config import get_yaml_config
from fastapi import APIRouter, status
from fastapi.responses import Response
# from fastapi_utils.cbv import cbv
from google.protobuf import json_format
import json
from loguru import logger
import grpc
from proto import reservation_crud_pb2_grpc, reservation_crud_pb2

router = APIRouter(
    tags=["Reservation"],
)


@router.get(
    "/all",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all reservations",
)
async def getAll():
    logger.info("Gateway processing getAll reservations");
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        logger.info("Gateway processing getAll reservation data");
        data = await stub.GetAll({});
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
    logger.info("Gateway processing getById Reservation request");
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.GetById(reservation_crud_pb2.ReservationId(id=item_id));
        if data.reservation_id == "":
            return Response(
                status_code=200, media_type="application/json", content="Invalid id"
            )
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )

@router.get(
    "/host/{host_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all reservations by host id",
)
async def getByHost(host_id):
    logger.info("Gateway processing getPendingByHostId Reservation request");
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
    "/host/pending/{host_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get pending reservations by host id",
)
async def getPendingByHost(host_id):
    logger.info("Gateway processing getPendingByHostId Reservation request");
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



@router.post(
    "/create",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Create new reservation",
)
async def create(item: ReservationDto):
    logger.info("Gateway processing create Availability request");

    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)

        reservation = reservation_crud_pb2.ReservationDto()
        reservation.reservation_id = str(item.reservation_id)
        reservation.accommodation_id = str(item.accommodation_id)
        reservation.host_id = str(item.host_id)
        reservation.guest_id = str(item.guest_id)
        reservation.number_of_guests = item.number_of_guests
        reservation.beginning_date = str(item.beginning_date)
        reservation.ending_date = str(item.ending_date)
        reservation.total_price = item.total_price
        reservation.status = item.status

        response = await stub.Create(reservation);

        if response.status == "Invalid date":
            return Response(
                status_code=200, media_type="application/json", content="Invalid date"
            )

    return Response(
        status_code=200, media_type="application/json", content="Success"
    )


@router.put(
    "/update",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update reservation",
)
async def update(item: ReservationDto):
    logger.info("Gateway processing update reservation request");
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:

        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)

        reservation = reservation_crud_pb2.ReservationDto()
        reservation.reservation_id = str(item.reservation_id)
        reservation.accommodation_id = str(item.accommodation_id)
        reservation.host_id = str(item.host_id)
        reservation.guest_id = str(item.guest_id)
        reservation.number_of_guests = item.number_of_guests
        reservation.beginning_date = str(item.beginning_date)
        reservation.ending_date = str(item.ending_date)
        reservation.total_price = item.total_price
        reservation.status = item.status

        response = await stub.Update(reservation);
    return Response(
        status_code=200, media_type="application/json", content=response.status
    )


@router.put(
    "/accept",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Accept a reservation",
)
async def AcceptReservation(item: ReservationDto):
    logger.info("Gateway processing accept reservation request");
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:

        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)

        reservation = reservation_crud_pb2.ReservationDto()
        reservation.reservation_id = str(item.reservation_id)
        reservation.accommodation_id = str(item.accommodation_id)
        reservation.host_id = str(item.host_id)
        reservation.guest_id = str(item.guest_id)
        reservation.number_of_guests = item.number_of_guests
        reservation.beginning_date = str(item.beginning_date)
        reservation.ending_date = str(item.ending_date)
        reservation.total_price = item.total_price
        reservation.status = item.status

        response = await stub.AcceptReservation(reservation);
        #after completing this step, adequate changes should be made in availability servicer

    return Response(
        status_code=200, media_type="application/json", content=response.status
    )

@router.delete(
    "/delete/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update reservation",
)
async def delete(item_id):
    logger.info("Gateway processing delete reservation request");
    reservation_server = (
            get_yaml_config().get("reservation_server").get("ip")
            + ":"
            + get_yaml_config().get("reservation_server").get("port")
    )
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        data = await stub.Delete(reservation_crud_pb2.ReservationId(id=item_id));
    return Response(
        status_code=200, media_type="application/json", content=data.status
    )
