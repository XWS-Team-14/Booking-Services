import uuid
from datetime import datetime, date

from proto import reservation_crud_pb2
from ..models.guest import Guest
from ..models.reservation import Reservation
from ..models.reservation_status import ReservationStatus


class ReservationHelper():
    def convertDate(date):
        # assuming iso YYYY-MM-DD date format3
        date_data = date.split('-')
        date_day = date_data[2].split(' ')
        return datetime(int(date_data[0]), int(date_data[1]), int(date_day[0]), hour=0, minute=0, second=0,
                        microsecond=0, tzinfo=None)

    def convertDateTime(datetime):
        # '2019-05-18T15:17:08.132263'
        return datetime.isoformat().split('T')[0]

    def convertGuestDto(request):
        return Guest(id = request.id,
                     canceledReservations = request.canceledReservations)

    def convertDto(request):
        beginning = ReservationHelper.convertDate(request.beginning_date)
        ending = ReservationHelper.convertDate(request.ending_date)
        status = ReservationStatus.PENDING
        if request.status == 3:
            status = ReservationStatus.ACCEPTED
        elif request.status == 1:
            status = ReservationStatus.REJECTED
        guest = Guest(id = request.guest.id, canceledReservations = request.guest.canceledReservations)
        return Reservation(
            id=request.reservation_id,
            accommodation_id=request.accommodation_id,
            host_id=request.host_id,
            guest=guest,
            number_of_guests=request.number_of_guests,
            beginning_date=beginning,
            ending_date=ending,
            total_price=request.total_price,
            status=status
        )

    def convertToDto(reservation):
        retVal = reservation_crud_pb2.ReservationDto()
        retVal.reservation_id = str(reservation.id)
        retVal.accommodation_id = str(reservation.accommodation_id)
        retVal.host_id = str(reservation.host_id)
        retVal.guest.id = str(reservation.guest.id)
        retVal.guest.canceledReservations = reservation.guest.canceledReservations
        retVal.number_of_guests = reservation.number_of_guests
        retVal.beginning_date = ReservationHelper.convertDateTime(reservation.beginning_date)
        retVal.ending_date = ReservationHelper.convertDateTime(reservation.ending_date)
        retVal.total_price = reservation.total_price
        retVal.status = reservation.status.value
        return retVal

    def convertGuestToDto(guest):
        retVal = reservation_crud_pb2.Guest()
        retVal.id = str(guest.id)
        retVal.canceledReservations = guest.canceledReservations
        return retVal

    def validateDates(start, end):
        return date.today() < start.date() < end.date()
