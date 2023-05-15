import uuid
from datetime import date, datetime

from beanie.exceptions import DocumentNotFound
from pydantic.datetime_parse import timedelta

from proto import reservation_crud_pb2_grpc, reservation_crud_pb2
from loguru import logger

from .reservation_helper import ReservationHelper
from ..models.accommodation import Accommodation
from ..models.guest import Guest
from ..models.reservation import Reservation
from ..models.reservation_status import ReservationStatus


class ReservationServicer(reservation_crud_pb2_grpc.ReservationCrudServicer):
    async def Create(self, request, context):
        logger.success('Request for creation of reservation accepted')
        reservation = ReservationHelper.convertDto(request)
        if not ReservationHelper.validateDates(reservation.beginning_date, reservation.ending_date):
            logger.exception('Dates are not valid')
            return reservation_crud_pb2.ReservationResult(status="Invalid date")
        reservation.id = uuid.uuid4()
        await reservation.insert()
        logger.success('reservation succesfully saved')
        return reservation_crud_pb2.ReservationResult(status="Success")

    async def CreateGuest(self, request, context):
        logger.success('Request for creation of guest accepted')
        guest = ReservationHelper.convertGuestDto(request)
        await guest.insert()
        logger.success('guest succesfully saved')
        return reservation_crud_pb2.ReservationResult(status="Success");

    async def CreateAccommodation(self, request, context):
        logger.success('Request for creation of accommodation accepted')
        accommodation = ReservationHelper.convertAccommodationDto(request)
        await accommodation.insert()
        logger.success('guest succesfully saved')
        return reservation_crud_pb2.ReservationResult(status="Success");

    async def Update(self, request, context):
        logger.success('Request for update of reservation accepted')
        reservation = ReservationHelper.convertDto(request)
        if not ReservationHelper.validateDates(reservation.beginning_date, reservation.ending_date):
            logger.exception('Dates are not valid')
            return reservation_crud_pb2.ReservationResult(status="Invalid date")
        try:
            item = await reservation.get(reservation.id)
            if not item:
                logger.info('Update failed, document with given id not found')
                return reservation_crud_pb2.ReservationResult(status="Failed, not found")
            await reservation.replace()
        except (ValueError, DocumentNotFound):
            logger.info('Update failed, document with given id not found')
            return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        logger.success('Reservation succesfully updated')
        return reservation_crud_pb2.ReservationResult(status="Success")

    async def UpdateGuest(self, request, context):
        logger.success('Request for update of guest accepted')
        guest = ReservationHelper.convertGuestDto(request)
        try:
            item = await guest.get(guest.id)
            if not item:
                logger.info('Update failed, document with given id not found')
                return reservation_crud_pb2.ReservationResult(status="Failed, not found")
            await guest.replace()
        except (ValueError, DocumentNotFound):
            logger.info('Update failed, document with given id not found')
            return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        logger.success('Reservation succesfully updated')
        return reservation_crud_pb2.ReservationResult(status="Success")

    async def UpdateAccommodation(self, request, context):
        logger.success('Request for update of accommodation accepted')
        accommodation = ReservationHelper.convertAccommodationDto(request)
        try:
            item = await accommodation.get(accommodation.id)
            if not item:
                logger.info('Update failed, document with given id not found')
                return reservation_crud_pb2.ReservationResult(status="Failed, not found")
            await accommodation.replace()
        except (ValueError, DocumentNotFound):
            logger.info('Update failed, document with given id not found')
            return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        logger.success('Reservation succesfully updated')
        return reservation_crud_pb2.ReservationResult(status="Success")

    async def Delete(self, request, context):
        logger.success('Request for deletion of Reservation accepted')
        try:
            item = await Reservation.get(uuid.UUID(request.id))
            if not item:
                logger.info('Delete failed, document with given id not found')
                return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        except (ValueError, DocumentNotFound):
            logger.info('Delete failed, document with given id not found')
            return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        if item.beginning_date <= (datetime.today() + timedelta(days=1)):
            return reservation_crud_pb2.ReservationResult(status = "You cannot cancel a reservation that is less than one day from now")
        guest = ReservationHelper.convertGuestDto(item.guest)
        guest.canceledReservations = guest.canceledReservations + 1
        await guest.replace()
        await item.delete()
        logger.success('reservation succesfully deleted')
        return reservation_crud_pb2.ReservationResult(status="Success")

    async def DeleteGuest(self, request, context):
        logger.success('Request for deletion of Guest accepted')
        try:
            item = await Guest.get(uuid.UUID(request.id))
            if not item:
                logger.info('Delete failed, document with given id not found')
                return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        except (ValueError, DocumentNotFound):
            logger.info('Delete failed, document with given id not found')
            return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        await item.delete()
        logger.success('guest succesfully deleted')
        return reservation_crud_pb2.ReservationResult(status="Success")

    async def DeleteAccommodation(self, request, context):
        logger.success('Request for deletion of Guest accepted')
        try:
            item = await Accommodation.get(uuid.UUID(request.id))
            if not item:
                logger.info('Delete failed, document with given id not found')
                return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        except (ValueError, DocumentNotFound):
            logger.info('Delete failed, document with given id not found')
            return reservation_crud_pb2.ReservationResult(status="Failed, not found")
        await item.delete()
        logger.success('guest succesfully deleted')
        return reservation_crud_pb2.ReservationResult(status="Success")

    async def GetAll(self, request, context):
        logger.success('Request for fetch all of reservation accepted')
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        logger.info('fetched data converting')
        for reservation in reservations:
            retVal.items.append(ReservationHelper.convertToDto(reservation))
        logger.success('Succesfully fetched')
        return retVal

    async def GetAllGuests(self, request, context):
        logger.success('Request for fetch all of guests accepted')
        guests = await Guest.find_all().to_list()
        retVal = reservation_crud_pb2.Guests()
        logger.info('fetched data converting')
        for guest in guests:
            retVal.items.append(ReservationHelper.convertGuestToDto(guest))
        logger.success('Succesfully fetched')
        return retVal

    async def GetByHost(self, request, context):
        logger.success('Request for fetching reservations by host accepted')
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        for reservation in reservations:
            reservation_dto = ReservationHelper.convertToDto(reservation)
            if reservation_dto.host_id == request.id:
                retVal.items.append(reservation_dto)
        return retVal

    async def GetActiveByHost(self,request,context):
        logger.success('Request for fetching active reservations by host accepted')
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        for reservation in reservations:
            if str(reservation.host_id) == request.id:
                if reservation.beginning_date >= datetime.now():
                    reservation_dto = ReservationHelper.convertToDto(reservation)
                    retVal.items.append(reservation_dto)
        return retVal

    async def GetByGuest(self, request, context):
        logger.success('Request for fetching reservations by guest accepted')
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        for reservation in reservations:
            reservation_dto = ReservationHelper.convertToDto(reservation)
            if reservation_dto.guest.id == request.id:
                retVal.items.append(reservation_dto)
        return retVal

    async def GetActiveByGuest(self,request, context):
        logger.success('Request for fetching reservations by guest accepted')
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos()
        for reservation in reservations:

            if str(reservation.guest.id) == request.id:
                if reservation.beginning_date >= datetime.now():
                    reservation_dto = ReservationHelper.convertToDto(reservation)
                    retVal.items.append(reservation_dto)
        return retVal

    async def GetReservationsForAcceptance(self,request,context):
        reservations = await Reservation.find_all().to_list()
        acceptedReservation = ReservationHelper.convertDto(request)
        retVal = []
        for reservation in reservations:
            if reservation.accommodation.id == acceptedReservation.accommodation.id:
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

    async def GetReservationsByAccommodation(self, request, context):
        reservations = await Reservation.find_all().to_list()
        retVal = reservation_crud_pb2.ReservationDtos
        for reservation in reservations:
            if str(reservation.accommodation.id) == request.id:
                retVal.items.append(ReservationHelper.convertToDto(reservation))
        return retVal

    async def AcceptReservation(self,request,context):
        reservations = await self.GetReservationsForAcceptance(request,context)
        if not reservations:
            return reservation_crud_pb2.ReservationResult(status="There are no requests that match those characteristics")
        for reservation in reservations:
            if str(reservation.id) == request.reservation_id:
                reservation.status = ReservationStatus.ACCEPTED
                reservation_dto = ReservationHelper.convertToDto(reservation)
                await self.Update(reservation_dto,context)
            else:
                reservation.status = ReservationStatus.REJECTED
                reservation_dto = ReservationHelper.convertToDto(reservation)
                await self.Update(reservation_dto,context)
        return reservation_crud_pb2.ReservationResult(status = "success")

    async def GetById(self, request, context):
        logger.success('Request for fetch reservation accepted')
        try:
            item = await Reservation.get(uuid.UUID(request.id))
        except (ValueError, DocumentNotFound):
            logger.info('Fetch failed, document with given id not found')
            return reservation_crud_pb2.ReservationDto()
        if not item:
            logger.info('fetched nothing')
            return reservation_crud_pb2.ReservationDto()
        else:
            logger.success('Succesfully fetched')
            return ReservationHelper.convertToDto(item)

    async def GetGuestById(self, request, context):
        logger.success('Request for fetch reservation accepted')
        try:
            item = await Guest.find_one(Guest.id == uuid.UUID(request.id))
        except (ValueError, DocumentNotFound):
            logger.info('Fetch failed, document with given id not found')
            return reservation_crud_pb2.Guest()
        if not item:
            logger.info('fetched nothing')
            return reservation_crud_pb2.Guest()
        else:
            logger.success('Succesfully fetched')
            return ReservationHelper.convertGuestToDto(item)

    async def GetAccommodationById(self, request, context):
        logger.success('Request for fetch reservation accepted')
        try:
            item = await Accommodation.find_one(Accommodation.id == uuid.UUID(request.id))
        except (ValueError, DocumentNotFound):
            logger.info('Fetch failed, document with given id not found')
            return reservation_crud_pb2.AccommodationResDto()
        if not item:
            logger.info('fetched nothing')
            return reservation_crud_pb2.AccommodationResDto()
        else:
            logger.success('Succesfully fetched')
            return ReservationHelper.convertAccommodationToDto(item)