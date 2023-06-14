import uuid

from app.core.availability_helper import AvailabilityHelper
from app.models.availability import Availability
from app.models.holiday import Holiday
from app.models.interval import Interval
from beanie.exceptions import DocumentNotFound
from beanie.operators import GTE, LTE
from loguru import logger

from proto import availability_crud_pb2, availability_crud_pb2_grpc



class AvailabilityServicer(availability_crud_pb2_grpc.AvailabilityCrudServicer):
    async def Create(self, request, context):
        logger.success("Request for creation of Availability accepted")
        availability = AvailabilityHelper.convert_dto(request)
        logger.info(availability)
        if not AvailabilityHelper.validate_dates(availability.available_interval):
            logger.exception("Dates are not valid")
            return availability_crud_pb2.Result(status="Invalid date")
        availability.id = uuid.uuid4()
        await availability.insert()
        logger.success("Availability succesfully saved")
        return availability_crud_pb2.Result(status="Success")

    async def Update(self, request, context):
        logger.success("Request for update of Availability accepted")
        availability = AvailabilityHelper.convert_dto(request)
        if not AvailabilityHelper.validate_dates(availability.available_interval):
            logger.exception("Dates are not valid")
            return availability_crud_pb2.Result(status="Invalid date")
        try:
            item = await Availability.get(str(availability.id))
            if not item:
                logger.info("Update failed, document with given id not found")
                return availability_crud_pb2.Result(status="Failed, not found")
            if item.occupied_intervals:
                logger.info("Update failed, availability has reservations")
                return availability_crud_pb2.Result(status="Failed, has reservations")
            await availability.replace()
        except (ValueError, DocumentNotFound):
            logger.info("Update failed, document with given id not found")
            return availability_crud_pb2.Result(status="Failed, not found")
        logger.success("Availability succesfully updated")
        return availability_crud_pb2.Result(status="Success")

    async def Delete(self, request, context):
        logger.success("Request for deletion of Availability accepted")
        try:
            item = await Availability.get(request.id)
            if not item:
                logger.info("Delete failed, document with given id not found")
                return availability_crud_pb2.Result(status="Failed, not found")
            if item.occupied_intervals:
                logger.info("Delete failed, availability has reservations")
                return availability_crud_pb2.Result(status="Failed, has reservations")
        except (ValueError, DocumentNotFound):
            logger.info("Delete failed, document with given id not found")
            return availability_crud_pb2.Result(status="Failed, not found")
        await item.delete()
        logger.success("Availability succesfully deleted")
        return availability_crud_pb2.Result(status="Success")

    async def GetAll(self, request, context):
        logger.success("Request for fetch all of Availability accepted")
        aas = await Availability.find_all().to_list()
        retVal = availability_crud_pb2.AvailabilityDtos()
        logger.info("fetched data converting")
        for aa in aas:
            retVal.items.append(AvailabilityHelper.convert_to_dto(aa))
        logger.success("Succesfully fetched")
        return retVal

    async def GetById(self, request, context):
        logger.success("Request for fetch Availability accepted")
        try:
            item = await Availability.get(request.id)
        except (ValueError, DocumentNotFound):
            logger.info("Fetch failed, document with given id not found")
            return availability_crud_pb2.AvailabilityDto()
        if not item:
            logger.info("fetched nothing")
            return availability_crud_pb2.AvailabilityDto()
        else:
            logger.success("Succesfully fetched")
            return AvailabilityHelper.convert_to_dto(item)

    async def GetByAccommodationId(self, request, context):
        logger.success("Request for fetch  availability by accommodation Id accepted")
        aas = await Availability.find_all().to_list()
        logger.info("fetched data converting")
        for aa in aas:
            if str(aa.accommodation_id) == request.id:
                return AvailabilityHelper.convert_to_dto(aa)
        logger.info("fetched nothing")
        return availability_crud_pb2.AvailabilityDto()

    async def GetAllSearch(self, request, context):
        logger.success("Request for search fetch Availability accepted")
        retVal = availability_crud_pb2.ExpandedAvailabilityDtos()
        if request.interval.date_start == "" or request.interval.date_end == "":
            logger.info("Some parts of request data are missing, fetching all")
            aas = await Availability.find_all().to_list()
            logger.info(aas)
            for aa in aas:
                retVal.items.append(AvailabilityHelper.convert_to_expanded_dto(aa))
            return retVal
        if not AvailabilityHelper.validate_dates(
            AvailabilityHelper.convert_date_interval(request.interval)
        ):
            logger.exception("Dates are not valid")
            return availability_crud_pb2.ExpandedAvailabilityDtos()
        list = await Availability.find(
            LTE(
                Availability.available_interval.date_start,
                AvailabilityHelper.convert_date(request.interval.date_start),
            ),
            GTE(
                Availability.available_interval.date_end,
                AvailabilityHelper.convert_date(request.interval.date_end),
            ),
        ).to_list()
        realList = [
            x for x in list if AvailabilityHelper.is_available(request.interval, x)
        ]
        holidays = await Holiday.find_all().to_list()
        for item in realList:
            retVal.items.append(AvailabilityHelper.convert_to_expanded_dto(item))
            print(AvailabilityHelper.calculate_price(
                request.interval, request.guests, item, holidays
            ))
            retVal.items[-1].total_price = AvailabilityHelper.calculate_price(
                request.interval, request.guests, item, holidays
            )
        logger.success("Succesfully fetched")
        return retVal

    async def AddOccupiedInterval(self, request, context):
        logger.success("Request for interval update accepted")
        try:
            item = await Availability.get(request.id)
        except (ValueError, DocumentNotFound):
            logger.exception("Fetch failed, document with given id not found")
            return availability_crud_pb2.Result(status="Failed, not found")
        if not item:
            logger.info("fetched nothing")
            return availability_crud_pb2.Result(status="Failed, not found")
        else:
            logger.success("Succesfully fetched")
            occ_intervals = []
            requested_interval = Interval(
                date_start=AvailabilityHelper.convert_date(request.interval.date_start),
                date_end=AvailabilityHelper.convert_date(request.interval.date_end),
            )
            if item.occupied_intervals is not None:
                logger.info("extending its not none")
                for interval in item.occupied_intervals:
                    if AvailabilityHelper.date_intersection(
                        requested_interval, interval
                    ):
                        logger.info("Interval has overlap, Failiure")
                        return availability_crud_pb2.Result(
                            status="Interval has overlap, Failiure"
                        )
                logger.info(item.occupied_intervals)
                occ_intervals.extend(item.occupied_intervals)

            occ_intervals.append(requested_interval)
            item.occupied_intervals = occ_intervals
            await item.replace()
            logger.success("Succesfully updated intervals")
            return availability_crud_pb2.Result(status="Success")

    async def RemoveOccupiedInterval(self, request, context):
        logger.success('Request for interval update accepted')
        try:
            item = await Availability.find_one(Availability.accommodation_id == uuid.UUID(request.id))
        except (ValueError, DocumentNotFound):
            logger.exception('Fetch failed, document with given id not found')
            return availability_crud_pb2.Result(status="Failed, not found")
        if not item:
            logger.info('fetched nothing')
            return availability_crud_pb2.Result(status="Failed, not found")
        else:
            logger.success('Successfully fetched')
            requested_interval = AvailabilityHelper.convert_date_interval(request.interval)
            if requested_interval in item.occupied_intervals:
                item.occupied_intervals.remove(requested_interval)
                await item.replace()
            logger.success('Succesfully updated intervals')
            return availability_crud_pb2.Result(status="Success")

    async def GetPrice(self, request, context):
        logger.success("Request for price calculation accepted")
        if request.interval.date_start == "" or request.interval.date_end == "" or request.guests == 0:
            logger.info("Some parts of request data are missing, discard request")
            return availability_crud_pb2.Price()
        interval = AvailabilityHelper.convert_date_interval(request.interval)
        logger.info(interval)
        if not AvailabilityHelper.validate_dates(interval):
            logger.exception("Dates are not valid")
            return availability_crud_pb2.Price()
        availability = await Availability.find_one(Availability.accommodation_id == uuid.UUID(request.accommodation_id))
        if availability is None:
             return availability_crud_pb2.Price()
        if not AvailabilityHelper.is_available(interval, availability):
            logger.exception("Isn't available")
            return availability_crud_pb2.Price()
        holidays = await Holiday.find_all().to_list()
        retVal = availability_crud_pb2.Price()
        retVal.price = AvailabilityHelper.calculate_price(
            request.interval, request.guests, availability, holidays
        )
        return retVal
