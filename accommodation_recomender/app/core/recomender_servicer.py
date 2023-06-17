import uuid
from app.models.models import ReviewRel
from app.models.models import User
from app.models.models import Accommodation
from app.db.neomodel import start_neomodel
from proto import accommodation_recomender_pb2_grpc, accommodation_recomender_pb2
from loguru import logger
from neomodel import Q
from datetime import datetime, timedelta, date
import time

class RecomenderServicer(accommodation_recomender_pb2_grpc.AccommodationRecomenderServicer):

    async def GetRecomended(self, request, context):
        start_neomodel()
        logger.success(f'Fetch recommended for user {request.id} request recieved')
        user = User.nodes.get(user_id=request.id)
        
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
            possible_accomodations.update(similar.reviewed.exclude(grade_lt=2))  #exclude those who have gotten grade less than 2 
        if len(possible_accomodations) == 0:
            logger.info(f'Found 0 possible accomodations returning empty') 
            return accommodation_recomender_pb2.Accommodation_ids(ids=[''])
        logger.info(f'Filtering with bad grades and attaching average grade')
        three_months_ago = date.today() - timedelta(days =3*30)
        three_months_ago = time.mktime(three_months_ago.timetuple())
        for possible_accomm in possible_accomodations:
            count = possible_accomm.reviewed.match(Q(grade__lt=3) & Q(timestamp__gte=three_months_ago)).count()
            if count > 5: 
                possible_accomodations.discard(possible_accomm)
            else:
                grades = [review.grade for review in possible_accomm.review.all()]
                possible_accomm.avg_grade = sum(grades) / len(grades) if grades else 1
        
        logger.info(f'Sorting and slicing 10 best')  
        logger.info(possible_accomodations)
        if len(possible_accomodations) != 0 :      
            sorted_accoms = list(possible_accomodations).sort(key=lambda obj: obj.avg_grade)
            best_accoms = sorted_accoms[:10]
            accom_ids = []
            for item in best_accoms:
                accom_ids.append(item.id)
            logger.info(f'Returnings ids: {accom_ids}') 
        else:
            logger.info(f'Found none returning empty') 
        return accommodation_recomender_pb2.Accommodation_ids(ids=[''])
