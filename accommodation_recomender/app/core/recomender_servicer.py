import uuid
from app.models.models import User
from app.models.models import Accommodation
from app.db.neomodel import start_neomodel
from proto import accommodation_recomender_pb2_grpc, accommodation_recomender_pb2
from loguru import logger


class RecomenderServicer(accommodation_recomender_pb2_grpc.AccommodationRecomenderServicer):

    async def GetRecomended(self, request, context):
        start_neomodel()
        logger.success(f'Fetch recommended for user {request.id} request recieved')
        # compute data and stuff
        jim = User(user_id = request.id, first_name='Jim', last_name='djobajden').save()
        aaaa = Accommodation(accomodation_id = str(uuid.uuid4()), name='AAAAAAAAAAA').save() 
        logger.success('logged')
        
        jim.reserved.connect(aaaa);
        aaaa.is_reserved.connect(jim);
        
        users = User.nodes.all()
        logger.info(users)
        acomod = Accommodation.nodes.first(name='AAAAAAAAAAA')
        logger.info(acomod)
        
        for acuser in acomod.is_reserved.all():
            logger.info(acuser)
        
        return accommodation_recomender_pb2.Accommodation_ids(ids=['asd'])
