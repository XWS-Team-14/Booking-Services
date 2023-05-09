import uuid
from availability.app.core.availability_helper import AvailabilityHelper
from availability.app.models.availability import Availability

from proto import availability_crud_pb2_grpc, availability_crud_pb2
from loguru import logger

from beanie.exceptions import DocumentNotFound

class AvailabilityServicer(availability_crud_pb2_grpc.AvailabilityCrudServicer):
    async def Create(self, request, context):
        logger.success('Request for creation of Availability accepted');
        availability = AvailabilityHelper.convertDto(request);
        await availability.insert()
        logger.success('Availability succesfully saved');
        return availability_crud_pb2.Result(status ="Success");
    
    async def Update(self, request, context):
        logger.success('Request for update of Availability accepted');
        availability = AvailabilityHelper.convertDto(request);
        try:
            item = await Availability.get(availability.availability_id);
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
        item.delete();
        logger.success('Availability succesfully deleted');
        return availability_crud_pb2.Result(status ="Success");
        
    async def GetAll(self, request, context):
        logger.success('Request for fetch all of Availability accepted');
        aas = await Availability.find_all()
        retVal = availability_crud_pb2.AvailabilityDtos();
        for aa in aas :
            retVal.append(AvailabilityHelper.convertToDto(aa));
        logger.success('Succesfully fetched');
        return retVal;
    
    async def GetById(self, request, context):
        logger.success('Request for fetch Availability accepted');
        try:
            item = await Availability.get(request.id);
        except (ValueError, DocumentNotFound):
            logger.exception('Fetch failed, document with given id not found');
            return availability_crud_pb2.Result(status ="Failed, not found");
        logger.success('Succesfully fetched');
        return AvailabilityHelper.convertToDto(item);
    
    async def GetAllSearch(self, request, context):
        logger.success('Request for search fetch Availability accepted');
        list = await Availability.find(
            Availability.available_interval.date_start.date < request.interval.date_start.date,
            Availability.available_interval.date_end.date > request.interval.date_end.date,
        )
        realList = [x for x in list if not AvailabilityHelper.isAvailable(request.interval,x)]
        for item in realList:
            item.base_price = AvailabilityHelper.calculatePrice(request.interval, request.num_of_guests, item);
        ## you need to fetch acomodation service to check min/max guest numbers
        return list;
            