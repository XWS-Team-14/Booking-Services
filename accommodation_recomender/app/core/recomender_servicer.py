import uuid
from app.models.models import ReviewRel
from app.models.models import User
from app.models.models import Accommodation
from app.db.neomodel import start_neomodel
from proto import accommodation_recomender_pb2_grpc, accommodation_recomender_pb2
from loguru import logger
from neomodel import Q
from datetime import datetime, timedelta, date
from google.protobuf.json_format import Parse
import json
import time

class RecomenderServicer(accommodation_recomender_pb2_grpc.AccommodationRecomenderServicer):

    async def GetRecomended(self, request, context):
        start_neomodel()
        logger.success(f'Fetch recommended for user {request.id} request recieved')
        try:
            user = User.nodes.get(user_id=request.id)
        except:
            return accommodation_recomender_pb2.Accommodation_ids(ids=[''])
        #assuming that user who made a review visited, but other way arrount is not true
        logger.info(f'Fetching similar users')
        similar_users = set()
        accommodations_reviewed = user.reviewed.all() 
        for accommodation in accommodations_reviewed:
            grade_by_user = user.reviewed.relationship(accommodation).grade
            similar_users.update(accommodation.is_reviewed.match(grade=grade_by_user))
            
        similar_users.discard(user)
        if len(similar_users) == 0:
            logger.info(f'Found 0 similar users returning empty') 
            return accommodation_recomender_pb2.Accommodation_ids(ids=[''])
        
        logger.info(f'Fetching possible accommodations')
        possible_accomodations = set()
        for similar in similar_users:
            possible_accomodations.update(similar.reviewed.match(grade__gte=3))  #exclude those who have gotten grade less than 2 
       
        if len(possible_accomodations) == 0:
            logger.info(f'Found 0 possible accomodations returning empty') 
            return accommodation_recomender_pb2.Accommodation_ids(ids=[''])
        
        logger.info(f'Filtering with bad grades, visited by user and attaching average grade')
        logger.info(possible_accomodations)
        three_months_ago = datetime.today() - timedelta(days =3*30)
        #three_months_ago = time.mktime(three_months_ago.timetuple())
        
        final_accomodations = []
        for possible_accomm in possible_accomodations:
            if possible_accomm.is_reserved.is_connected(user):
                continue
            count = len(possible_accomm.is_reviewed.match(grade__lt=3,timestamp__gte=three_months_ago))
            if count > 5: 
                continue
            else:
                logger.info('Calculating avg grade')
                helper_users = possible_accomm.is_reviewed.all() 
                grades = [] 
                for h_user in helper_users:
                    grades.append(possible_accomm.is_reviewed.relationship(h_user).grade)
                possible_accomm.avg_grade = sum(grades) / len(grades) if grades else 1
                final_accomodations.append(possible_accomm)
        
        logger.info(f'Sorting and slicing 10 best')  
        logger.info(final_accomodations)
        if len(final_accomodations) != 0 :   
            final_accomodations.sort(key=lambda obj: obj.avg_grade)
            best_accoms = final_accomodations[:10]
            accom_ids = []
            for item in best_accoms:
                accom_ids.append(item.accomodation_id)
            logger.info(f'Returnings ids: {accom_ids}') 

            return accommodation_recomender_pb2.Accommodation_ids(ids = accom_ids)
        else:
            logger.info(f'Found none returning empty') 
            return accommodation_recomender_pb2.Accommodation_ids()
       
