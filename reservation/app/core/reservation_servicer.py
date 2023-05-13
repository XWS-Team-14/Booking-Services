import uuid
from datetime import date, datetime

from beanie.exceptions import DocumentNotFound

from proto import reservation_crud_pb2_grpc, reservation_crud_pb2
from loguru import logger

from .reservation_helper import ReservationHelper
from ..models.reservation import Reservation
from ..models.reservation_status import ReservationStatus


class ReservationServicer(reservation_crud_pb2_grpc.ReservationCrudServicer):
    async def Create(self, request, context):
        logger.success('Request for creation of reservation accepted');
        reservation = ReservationHelper.convertDto(request);
        if not ReservationHelper.validateDates(reservation.beginning_date, reservation.ending_date):
            logger.exception('Dates are not valid');
            return reservation_crud_pb2.Result(status="Invalid date");
        reservation.id = uuid.uuid4()
        await reservation.insert()
        logger.success('reservation succesfully saved');
        return reservation_crud_pb2.Result(status="Success");

    async def Update(self, request, context):
        logger.success('Request for update of reservation accepted');
        reservation = ReservationHelper.convertDto(request);
        if not ReservationHelper.validateDates(reservation.beginning_date, reservation.ending_date):
            logger.exception('Dates are not valid');
            return reservation_crud_pb2.Result(status="Invalid date");
        try:
            item = await reservation.get(reservation.id);
            if not item:
                logger.info('Update failed, document with given id not found');
                return reservation_crud_pb2.Result(status="Failed, not found");
            await reservation.replace()
        except (ValueError, DocumentNotFound):
            logger.info('Update failed, document with given id not found');
            return reservation_crud_pb2.Result(status="Failed, not found");
        logger.success('Reservation succesfully updated');
        return reservation_crud_pb2.Result(status="Success");

    async def Delete(self, request, context):
        logger.success('Request for deletion of Reservation accepted');
        try:
            item = await Reservation.get(request.id);
            if not item:
                logger.info('Delete failed, document with given id not found');
                return reservation_crud_pb2.Result(status="Failed, not found");
        except (ValueError, DocumentNotFound):
            logger.info('Delete failed, document with given id not found');
            return reservation_crud_pb2.Result(status="Failed, not found");
        await item.delete();
        logger.success('reservation succesfully deleted');
        return reservation_crud_pb2.Result(status="Success");

    async def GetAll(self, request, context):
        logger.success('Request for fetch all of reservation accepted');
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        logger.info('fetched data converting')
        for reservation in reservations:
            retVal.items.append(ReservationHelper.convertToDto(reservation));
        logger.success('Succesfully fetched');
        return retVal;

    async def GetByHost(self, request, context):
        logger.success('Request for fetching reservations by host accepted');
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        for reservation in reservations:
            reservation_dto = ReservationHelper.convertToDto(reservation)
            if reservation_dto.host_id == request.id:
                retVal.items.append(reservation_dto)
        return retVal

    async def GetByGuest(self, request, context):
        logger.success('Request for fetching reservations by host accepted');
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        for reservation in reservations:
            reservation_dto = ReservationHelper.convertToDto(reservation)
            if reservation_dto.guest_id == request.guest_id:
                retVal.items.append(reservation_dto)
        return retVal

    async def GetReservationsForAcceptance(self,request,context):
        reservations = await Reservation.find_all().to_list()
        acceptedReservation = ReservationHelper.convertDto(request)
        retVal = []
        for reservation in reservations:
            if reservation.accommodation_id == acceptedReservation.accommodation_id:
                if (reservation.beginning_date >= acceptedReservation.beginning_date and reservation.beginning_date <= acceptedReservation.ending_date)\
                        or (reservation.beginning_date <= acceptedReservation.beginning_date and reservation.ending_date >= acceptedReservation.ending_date)\
                        or (reservation.ending_date >= acceptedReservation.beginning_date and reservation.ending_date <= acceptedReservation.ending_date):
                    if(reservation.status == ReservationStatus.PENDING):

                        retVal.append(reservation)
        return retVal

    async def GetPendingReservationsByHost(self,request,context):
        reservations = await self.GetByHost(request,context)
        pendingReservations = reservation_crud_pb2.ReservationDtos()
        for reservation_dto in reservations.items:
            reservation = ReservationHelper.convertDto(reservation_dto)
            if reservation.status == ReservationStatus.PENDING and reservation.beginning_date > datetime.now():
                pendingReservations.items.append(ReservationHelper.convertToDto(reservation))
        return pendingReservations



    async def AcceptReservation(self,request,context):
        reservations = await self.GetReservationsForAcceptance(request,context)
        if not reservations:
            return reservation_crud_pb2.Result(status="There are no requests that match those characteristics");
        for reservation in reservations:
            if str(reservation.id) == request.reservation_id:
                reservation.status = ReservationStatus.ACCEPTED
                reservation_dto = ReservationHelper.convertToDto(reservation)
                await self.Update(reservation_dto,context)
            else:
                reservation.status = ReservationStatus.REJECTED
                reservation_dto = ReservationHelper.convertToDto(reservation)
                await self.Update(reservation_dto,context)
        return reservation_crud_pb2.Result(status = "success");

    async def GetById(self, request, context):
        logger.success('Request for fetch reservation accepted');
        try:
            item = await Reservation.get(request.id);
        except (ValueError, DocumentNotFound):
            logger.info('Fetch failed, document with given id not found');
            return reservation_crud_pb2.ReservationDto();
        if not item:
            logger.info('fetched nothing');
            return reservation_crud_pb2.ReservationDto();
        else:
            logger.success('Succesfully fetched');
            return ReservationHelper.convertToDto(item);
