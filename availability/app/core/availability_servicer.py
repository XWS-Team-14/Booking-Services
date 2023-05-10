import uuid
from app.core.availability_helper import AvailabilityHelper
from app.models.availability import Availability
from app.models.interval import Interval

from proto import availability_crud_pb2_grpc, availability_crud_pb2
from loguru import logger
from beanie import PydanticObjectId 

from beanie.exceptions import DocumentNotFound

class AvailabilityServicer(availability_crud_pb2_grpc.AvailabilityCrudServicer):
    async def Create(self, request, context):
        logger.success('Request for creation of Availability accepted');
        availability = AvailabilityHelper.convertDto(request);
        if not AvailabilityHelper.validateDates(availability.available_interval):
            logger.exception('Dates are not valid');
            return availability_crud_pb2.Result(status ="Invalid date");
        availability.id = uuid.uuid4()
        await availability.insert()
        logger.success('Availability succesfully saved');
        return availability_crud_pb2.Result(status ="Success");
    
    async def Update(self, request, context):
        logger.success('Request for update of Availability accepted');
        availability = AvailabilityHelper.convertDto(request);
        if not AvailabilityHelper.validateDates(availability.available_interval):
            logger.exception('Dates are not valid');
            return availability_crud_pb2.Result(status ="Invalid date");
        try:
            item = await Availability.get(availability.id);
            if not item.occupied_intervals:
                logger.exception('Update failed, availability has reservations');
                return availability_crud_pb2.Result(status ="Failed, has reservations");
            await availability.replace()
        except (ValueError, DocumentNotFound):
            logger.exception('Update failed, document with given id not found');
            return availability_crud_pb2.Result(status ="Failed, not found");
        logger.success('Availability succesfully updated');
        return availability_crud_pb2.Result(status ="Success");
    
    async def Delete(self, request, context):
        logger.success('Request for deletion of Availability accepted');
        try:
            item = await Availability.get(request.id);
            if not item.occupied_intervals:
                logger.exception('Update failed, availability has reservations');
                return availability_crud_pb2.Result(status ="Failed, has reservations");
        except (ValueError, DocumentNotFound):
            logger.exception('Delete failed, document with given id not found');
            return availability_crud_pb2.Result(status ="Failed, not found");
        await item.delete();
        logger.success('Availability succesfully deleted');
        return availability_crud_pb2.Result(status ="Success");
        
    async def GetAll(self, request, context):
        logger.success('Request for fetch all of Availability accepted');
        aas = await Availability.find_all().to_list()
        retVal = availability_crud_pb2.AvailabilityDtos()
        logger.info('fetched data converting')
        for aa in aas :
            retVal.items.append(AvailabilityHelper.convertToDto(aa));
        logger.success('Succesfully fetched');
        return retVal;
    
    async def GetById(self, request, context):
        logger.success('Request for fetch Availability accepted');
        try:
            item = await Availability.get(request.id);
        except (ValueError, DocumentNotFound):
            logger.info('Fetch failed, document with given id not found');
            return availability_crud_pb2.AvailabilityDto();
        if not item : 
            logger.info('fetched nothing');
            return availability_crud_pb2.AvailabilityDto();
        else : 
            logger.success('Succesfully fetched');
            return AvailabilityHelper.convertToDto(item);
    
    async def GetAllSearch(self, request, context):
        logger.success('Request for search fetch Availability accepted');
        if not AvailabilityHelper.validateDates(AvailabilityHelper.convertDateInterval(request.interval)):
            logger.exception('Dates are not valid');
            ## when dates are invalid responce is different
            return availability_crud_pb2.Result();
        list = await Availability.find(
            Availability.available_interval.date_start.date <= AvailabilityHelper.convertDate(request.interval.date_start).date,
            Availability.available_interval.date_end.date >= AvailabilityHelper.convertDate(request.interval.date_end).date,
        ).to_list()
        logger.success('Succesfully fetched list1');
        realList = [x for x in list if not AvailabilityHelper.isAvailable(request.interval,x)]
        logger.success('Succesfully fetched list2');
        for item in realList:
            item.base_price = AvailabilityHelper.calculatePrice(request.interval, request.num_of_guests, item);
        ## you need to fetch acomodation service to check min/max guest numbers
        logger.success('Succesfully fetched');
        return list;
    
    async def AddOccupiedInterval(self,request,context):
        logger.success('Request for interval update accepted');
        try:
            item = await Availability.get(request.id);
        except (ValueError, DocumentNotFound):
            logger.exception('Fetch failed, document with given id not found');
            return availability_crud_pb2.Result(status ="Failed, not found");
        await item.set({Availability.occupied_intervals:item.occupied_intervals.append(Interval(date_start = request.interval.date_start, date_end = request.interval.date_end))})
        logger.success('Succesfully updated intervals');
        return availability_crud_pb2.Result(status ="Success");
        
        