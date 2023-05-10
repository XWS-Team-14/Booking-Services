import uuid

from beanie.exceptions import DocumentNotFound

from proto import reservation_crud_pb2_grpc, reservation_crud_pb2
from loguru import logger

from .reservation_helper import ReservationHelper
from ..models.reservation import Reservation
from ..models.reservation_status import ReservationStatus


class ReservationServicer(reservation_crud_pb2_grpc.ReservationCrudServicer):
    async def Create(self, request, context):
        logger.success('Request for creation of Availability accepted');
        reservation = ReservationHelper.convertDto(request);
        if not ReservationHelper.validateDates(reservation.beginning_date, reservation.ending_date):
            logger.exception('Dates are not valid');
            return reservation_crud_pb2.Result(status="Invalid date");
        reservation.id = uuid.uuid4()
        await reservation.insert()
        logger.success('Availability succesfully saved');
        return reservation_crud_pb2.Result(status="Success");

    async def Update(self, request, context):
        logger.success('Request for update of Availability accepted');
        reservation = ReservationHelper.convertDto(request);
        if not ReservationHelper.validateDates(reservation.beginning_date, reservation.ending_date):
            logger.exception('Dates are not valid');
            return reservation_crud_pb2.Result(status="Invalid date");
        try:
            item = await reservation.get(str(reservation.id));
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
        logger.success('Availability succesfully deleted');
        return reservation_crud_pb2.Result(status="Success");

    async def GetAll(self, request, context):
        logger.success('Request for fetch all of Availability accepted');
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
            if reservation_dto.host_id.equals(request.host_id):
                retVal.items.append(reservation_dto)
        return retVal

    async def GetByGuest(self, request, context):
        logger.success('Request for fetching reservations by host accepted');
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        for reservation in reservations:
            reservation_dto = ReservationHelper.convertToDto(reservation)
            if reservation_dto.guest_id.equals(request.guest_id):
                retVal.items.append(reservation_dto)
        return retVal
    async def GetReservationsForAcceptance(self,request,context):
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        for reservation in reservations:
            reservation_dto = ReservationHelper.convertToDto(reservation)
            if reservation_dto.host_id.equals(request.host_id):
                if reservation_dto.beginning_date >= request.beginning_date and reservation_dto.ending_date <= request.ending_date:
                    if reservation_dto.accommodation_id.equals(request.accommodation_id):
                        retVal.items.append(reservation_dto)
        return retVal



    async def AcceptReservation(self,request,context):
        reservations = self.GetReservationsForAcceptance(self,request,context)
        for reservation in reservations:
            reservation_dto = ReservationHelper.convertToDto(reservation)
            if reservation_dto.id.equals(request.id):
                self.Update(self,reservation_dto,context)
            else:
                reservation_dto.status = ReservationStatus.REJECTED
                self.Update(self,reservation_dto,context)
        return reservation_crud_pb2.Result(status="Success");

    async def GetById(self, request, context):
        logger.success('Request for fetch Availability accepted');
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
