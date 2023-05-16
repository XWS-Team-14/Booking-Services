from datetime import datetime, date, timedelta
from app.models.availability import Availability
from app.models.interval import Interval
from app.models.pricing_type import PricingTypeEnum
from app.models.special_pricing import SpecialPricing
from proto import availability_crud_pb2
from loguru import logger


class AvailabilityHelper:
    def convertDate(date):
        # assuming iso YYYY-MM-DD date format3
        date_data = date.split("-")
        return datetime(
            int(date_data[0]),
            int(date_data[1]),
            int(date_data[2]),
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=None,
        )

    def convertDateTime(datetime):
        #'2019-05-18T15:17:08.132263'
        return datetime.isoformat().split("T")[0]

    def convertDateInterval(interval):
        return Interval(
            date_start=AvailabilityHelper.convertDate(interval.date_start),
            date_end=AvailabilityHelper.convertDate(interval.date_end),
        )

    def convertDto(request):
        special_pricing_list = list()
        ocuppied_intervals_list = list()

        if request.special_pricing:
            for item in request.special_pricing:
                special_pricing_list.append(
                    SpecialPricing(title=item.title, pricing_markup=item.pricing_markup)
                )

        if request.occupied_intervals:
            for item in request.occupied_intervals:
                ocuppied_intervals_list.append(
                    Interval(
                        date_start=AvailabilityHelper.convertDate(item.date_start),
                        date_end=AvailabilityHelper.convertDate(item.date_end),
                    )
                )

        return Availability(
            id=request.availability_id,
            accommodation_id=request.accommodation_id,
            available_interval=Interval(
                date_start=AvailabilityHelper.convertDate(request.interval.date_start),
                date_end=AvailabilityHelper.convertDate(request.interval.date_end),
            ),
            pricing_type=PricingTypeEnum[request.pricing_type],
            base_price=request.base_price,
            special_pricing=special_pricing_list,
            occupied_intervals=ocuppied_intervals_list,
        )

    def convertToDto(availability):
        retVal = availability_crud_pb2.AvailabilityDto()
        retVal.availability_id = str(availability.id)
        retVal.accommodation_id = str(availability.accommodation_id)
        retVal.interval.date_end = AvailabilityHelper.convertDateTime(
            availability.available_interval.date_end
        )
        retVal.interval.date_start = AvailabilityHelper.convertDateTime(
            availability.available_interval.date_start
        )
        retVal.pricing_type = availability.pricing_type.name
        retVal.base_price = availability.base_price
        special_pricing_list = list()
        ocuppied_intervals_list = list()
        if availability.special_pricing:
            for item in availability.special_pricing:
                pricing = availability_crud_pb2.SpecialPricing()
                pricing.title = item.title
                pricing.pricing_markup = item.pricing_markup
                special_pricing_list.append(pricing)
            retVal.special_pricing.extend(special_pricing_list)
        if availability.occupied_intervals:
            for item in availability.occupied_intervals:
                interval = availability_crud_pb2.Interval()
                interval.date_start = AvailabilityHelper.convertDateTime(
                    item.date_start
                )
                interval.date_end = AvailabilityHelper.convertDateTime(item.date_end)
                ocuppied_intervals_list.append(interval)
            retVal.occupied_intervals.extend(ocuppied_intervals_list)
        return retVal

    def convertToExpandedDto(availability):
        retVal = availability_crud_pb2.ExpandedAvailabilityDto()
        retVal.availability_id = str(availability.id)
        retVal.accommodation_id = str(availability.accommodation_id)
        retVal.interval.date_end = AvailabilityHelper.convertDateTime(
            availability.available_interval.date_end
        )
        retVal.interval.date_start = AvailabilityHelper.convertDateTime(
            availability.available_interval.date_start
        )
        retVal.pricing_type = availability.pricing_type.name
        retVal.base_price = availability.base_price
        retVal.total_price = availability.base_price
        special_pricing_list = list()
        ocuppied_intervals_list = list()
        if availability.special_pricing:
            for item in availability.special_pricing:
                pricing = availability_crud_pb2.SpecialPricing()
                pricing.title = item.title
                pricing.pricing_markup = item.pricing_markup
                special_pricing_list.append(pricing)
            retVal.special_pricing.extend(special_pricing_list)
        if availability.occupied_intervals:
            for item in availability.occupied_intervals:
                interval = availability_crud_pb2.Interval()
                interval.date_start = AvailabilityHelper.convertDateTime(
                    item.date_start
                )
                interval.date_end = AvailabilityHelper.convertDateTime(item.date_end)
                ocuppied_intervals_list.append(interval)
            retVal.occupied_intervals.extend(ocuppied_intervals_list)
        return retVal

    def isAvailable(requested_interval, availability):
        for interval in availability.occupied_intervals:
            if AvailabilityHelper.dateIntersection(
                interval, AvailabilityHelper.convertDateInterval(requested_interval)
            ):
                return False
        return True

    def dateIntersection(intervalA, intervalB):
        # (StartA <= EndB) and (EndA >= StartB)
        if (
            intervalA.date_start.date() <= intervalB.date_end.date()
            and intervalA.date_end.date() >= intervalB.date_start.date()
        ):
            return True
        return False

    def calculatePrice(requested_interval, num_of_guests, availability, holidays):
        # logger.info("price for - " + str(availability.base_price));
        guest_mul = 1
        price = 0
        requested_interval_date = AvailabilityHelper.convertDateInterval(
            requested_interval
        )
        if availability.pricing_type.name == "Per_guest":
            guest_mul = num_of_guests
        if not availability.special_pricing:
            # list of special price modifiers is empty
            return (
                (
                    (
                        requested_interval_date.date_end.date()
                        - requested_interval_date.date_start.date()
                    ).days
                    + 1
                )
                * availability.base_price
                * guest_mul
            )
        else:
            holiday_mul = AvailabilityHelper.getSpecialPrice(availability, "Holiday")
            weekend_mul = AvailabilityHelper.getSpecialPrice(availability, "Weekend")
            for day_num in range(
                (
                    requested_interval_date.date_end.date()
                    - requested_interval_date.date_start.date()
                ).days
                + 1
            ):
                curr_date = requested_interval_date.date_start.date() + timedelta(
                    day_num
                )
                # logger.info("curr=date" + str(curr_date))
                if AvailabilityHelper.isHoliday(curr_date, holidays):
                    # logger.info("hollidayy")
                    price = price + (availability.base_price * guest_mul * holiday_mul)
                    logger.info(price)
                    continue
                if AvailabilityHelper.isWeekend(curr_date):
                    # logger.info("weeekend")
                    price = price + (availability.base_price * guest_mul * weekend_mul)
                    # logger.info(price)
                    continue
                price = price + availability.base_price * guest_mul
                # logger.info(price)
        return price

    def isWeekend(date):
        if date.weekday() > 4:
            return True
        return False

    def isHoliday(date, holidays):
        for holiday in holidays:
            if holiday.date.date() == date:
                return True
        return False

    def getSpecialPrice(availability, title):
        for special_price in availability.special_pricing:
            if special_price.title == title:
                return special_price.pricing_markup
        return 1

    def validateDates(interval):
        return (
            interval.date_start.date() > date.today()
            and interval.date_start.date() < interval.date_end.date()
        )
