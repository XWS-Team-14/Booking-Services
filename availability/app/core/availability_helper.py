import datetime
from availability.app.models.availability import Availability
from availability.app.models.interval import Interval
from availability.app.models.pricing_type import PricingTypeEnum
from availability.app.models.special_pricing import SpecialPricing
from proto import availability_crud_pb2


class AvailabilityHelper():
    def convertDate(date):
        #assuming iso YYYY-MM-DD date format3
        date_data = date.split('-')
        return datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]), hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        
    def convertDateTime(datetime):
        #'2019-05-18T15:17:08.132263'
        return datetime.isoformat().split('T')[0]
    
    def convertDto(request):
        special_pricing_list = list()
        ocuppied_intervals_list = list()
        if request.HasField('special_pricing'):
            for item in request.special_pricing:
                special_pricing_list.append(SpecialPricing(titile = item.title, pricing_markup = item.pricing_markup))
        if request.HasField('occupied_intervals'):
            for item in request.occupied_intervals:
                ocuppied_intervals_list.append(Interval(date_start = item.date_start, date_end = item.date_end))
        return Availability(
            availability_id = request.availability_id,
            accomodation_id = request.accomodation_id,
            available_interval = Interval(date_start = request.interval.date_start, date_end = request.interval.date_end),
            pricing_type = PricingTypeEnum[request.pricing_type],
            base_price = request.base_price,
            special_pricing = special_pricing_list,
            occupied_intervals = ocuppied_intervals_list
        )
        
    def convertToDto(availability):
        retVal = availability_crud_pb2.AvailabilityDto()
        retVal.availability_id = availability.availability_id
        retVal.accomodation_id = availability.accomodation_id
        interval = availability_crud_pb2.Interval()
        interval.date_start = availability.available_interval.date_start
        interval.date_end = availability.available_interval.date_end
        retVal.interval = interval;
        retVal.pricing_type = availability.pricing_type.name
        retVal.base_price = availability.base_price
        special_pricing_list = list()
        ocuppied_intervals_list = list()
        for item in availability.special_pricing:
            pricing = availability_crud_pb2.SpecialPricing()
            pricing.title = item.title
            pricing.pricing_markup = item.pricing_markup
            special_pricing_list.append(pricing)
        retVal.special_pricing = special_pricing_list
        for item in availability.occupied_intervals:
            interval = availability_crud_pb2.Interval()
            interval.date_start = item.date_start
            interval.date_end = item.date_end
            ocuppied_intervals_list.append(interval)
        retVal.occupied_intervals = ocuppied_intervals_list
        return retVal
        
