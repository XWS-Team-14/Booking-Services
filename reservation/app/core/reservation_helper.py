from datetime import datetime, date

from proto import reservation_crud_pb2
from ..models.reservation import Reservation
from ..models.reservation_status import ReservationStatus


class ReservationHelper():
    def convertDate(date):
        # assuming iso YYYY-MM-DD date format3
        date_data = date.split('-')
        return datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]), hour=0, minute=0, second=0,
                        microsecond=0, tzinfo=None)

    def convertDateTime(datetime):
        # '2019-05-18T15:17:08.132263'
        return datetime.isoformat().split('T')[0]

    def convertDto(request):
        beginning = ReservationHelper.convertDate(request.beginning_date);
        ending = ReservationHelper.convertDate(request.ending_date);
        status = ReservationStatus.PENDING;
        if request.status.equals("ACCEPTED"):
            status = ReservationStatus.ACCEPTED
        elif request.status.equals("REJECTED"):
            status = ReservationStatus.REJECTED
        return Reservation(
            id=request.availability_id,
            accomodation_id=request.accomodation_id,
            host_id=request.host_id,
            guest_id=request.guest_id,
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
        retVal.guest_id = str(reservation.guest_id)
        retVal.number_of_guests = reservation.number_of_guests
        retVal.beginning_date = ReservationHelper.convertDateTime(reservation.beginning)
        retVal.ending_date = ReservationHelper.convertDateTime(reservation.ending)
        retVal.total_price = reservation.total_price
        return retVal

    def validateDates(start, end):
        return date.today() < start.date() < end.date()
