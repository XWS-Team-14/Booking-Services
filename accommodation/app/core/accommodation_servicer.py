from app.models.accommodation import Accommodation
from app.models.location import Location
from proto import accommodation_crud_pb2_grpc, accommodation_crud_pb2
from loguru import logger
import uuid


class AccommodationServicer(accommodation_crud_pb2_grpc.AccommodationCrudServicer):
    async def Delete(self, request, context):
        logger.info("Delete request started")
        try:
            obj_to_delete = await Accommodation.find_one(id == request.id)
        except Exception:
            logger.error("Trying to delete object that does not exist")
            return accommodation_crud_pb2.Empty()
        await obj_to_delete.delete()
        logger.success(f"Deleted an object with id = {request.id}")
        return accommodation_crud_pb2.Empty()

    async def DeleteByUser(self, request, context):
        logger.info("Delete request started")
        try:
            obj_to_delete = await Accommodation.find(
                Accommodation.user_id == uuid.UUID(request.id)
            )
        except Exception as e:
            logger.error(f"Trying to delete object that does not exist {e}")
            return accommodation_crud_pb2.Empty()
        await obj_to_delete.delete()
        logger.success(f"Deleted an object with id = {request.id}")
        return accommodation_crud_pb2.Empty()

    async def Create(self, request, context):
        logger.info("Create request started")
        try:
            obj = self.convert_from_dto(request)
            await obj.insert()
        except Exception as e:
            logger.error(f"Error creating object {e}")
            return accommodation_crud_pb2.Empty()
        logger.success(f"Created object with id = {request.id}")
        return accommodation_crud_pb2.Empty()

    async def Update(self, request, context):
        logger.info("Update request started")
        try:
            new_obj = self.convert_from_dto(request)
            await Accommodation.find_one(id=new_obj.id)
            new_obj.replace()
        except Exception:
            logger.error("Trying to update object that does not exist")
            return accommodation_crud_pb2.Empty()
        logger.success(f"Updated an object with id = {request.id}")
        return accommodation_crud_pb2.Empty()

    async def GetAll(self, request, context):
        logger.info("GetAll request started")
        try:
            objs = await Accommodation.find().to_list()
        except Exception:
            logger.error("Error getting accommodations")
            return accommodation_crud_pb2.Accommodations()
        transformed_objs = accommodation_crud_pb2.Accommodations()
        for obj in objs:
            transformed_objs.items.append(self.convert_to_dto(obj))
        return transformed_objs

    async def GetById(self, request, context):
        logger.info("GetById request started")
        try:
            obj_to_return = await Accommodation.get(request.id)
        except Exception as e:
            logger.error(f"Trying to get object that does not exist {e}")
            return accommodation_crud_pb2.Accommodation()
        accommodation = self.convert_to_dto(obj_to_return)
        return accommodation

    async def GetByLocation(self, request, context):
        logger.info("GetByLocation request started")
        try:
            location = self.convert_from_dto_location(request)
            objs = await Accommodation.find_all().to_list()
            updated_list = []
            if location.city != "":
                for obj in objs:
                    if obj.location.city == location.city:
                        updated_list.append(obj)
                objs = updated_list.copy()
            if location.country != "":
                for obj in objs:
                    if obj.location.country == location.country:
                        updated_list.append(obj)
                objs = updated_list.copy()
                updated_list = []
            if location.address != "":
                for obj in objs:
                    if obj.location.address == location.address:
                        updated_list.append(obj)
                objs = updated_list.copy()
                updated_list = []
        except Exception as e:
            logger.error(f"Error getting accommodations {e}")
            return accommodation_crud_pb2.Accommodations()
        transformed_objs = accommodation_crud_pb2.Accommodations()
        for obj in objs:
            transformed_objs.items.append(self.convert_to_dto(obj))
        return transformed_objs

    async def GetByUser(self, request, context):
        logger.info("GetByUser request started")
        try:
            objs = await Accommodation.find(
                Accommodation.user_id == uuid.UUID(request.id)
            )
        except Exception as e:
            logger.error(f"Trying to delete object that does not exist {e}")
            return accommodation_crud_pb2.Empty()
        transformed_objs = accommodation_crud_pb2.Accommodations()
        for obj in objs:
            transformed_objs.items.append(self.convert_to_dto(obj))
        return transformed_objs

    def convert_to_dto(
        self,
        obj_to_return: Accommodation,
    ) -> accommodation_crud_pb2.Accommodation:
        location = accommodation_crud_pb2.Location(
            country=obj_to_return.location.country,
            city=obj_to_return.location.city,
            address=obj_to_return.location.address,
        )
        features_list = list()
        image_urls_list = list()

        for item in obj_to_return.features:
            features_list.append(item)
        for item in obj_to_return.image_urls:
            image_urls_list.append(item)

        return accommodation_crud_pb2.Accommodation(
            id=str(obj_to_return.id),
            user_id=str(obj_to_return.user_id),
            name=obj_to_return.name,
            location=location,
            features=features_list,
            image_urls=image_urls_list,
            min_guests=obj_to_return.min_guests,
            max_guests=obj_to_return.max_guests,
        )

    def convert_from_dto(
        self,
        obj_to_return: accommodation_crud_pb2.Accommodation,
    ) -> Accommodation:
        location = Location(
            country=obj_to_return.location.country,
            city=obj_to_return.location.city,
            address=obj_to_return.location.address,
        )
        features_list = list()
        image_urls_list = list()

        for item in obj_to_return.features:
            features_list.append(item)
        for item in obj_to_return.image_urls:
            image_urls_list.append(item)

        return Accommodation(
            id=obj_to_return.id,
            user_id=obj_to_return.user_id,
            name=obj_to_return.name,
            location=location,
            features=features_list,
            image_urls=image_urls_list,
            min_guests=obj_to_return.min_guests,
            max_guests=obj_to_return.max_guests,
        )

    def convert_from_dto_location(
        self,
        obj_to_return: accommodation_crud_pb2.Location,
    ) -> Location:
        return Location(
            country=obj_to_return.country,
            city=obj_to_return.city,
            address=obj_to_return.address,
        )
