from neomodel import (StructuredNode,StructuredRel,DateTimeProperty, StringProperty,Relationship,ArrayProperty,IntegerProperty,BooleanProperty)
from datetime import datetime

class ReviewRel(StructuredRel):
    timestamp = DateTimeProperty(
        index=True
    )
    grade = IntegerProperty()
    
class User(StructuredNode):
    user_id = StringProperty(unique_index=True, required=True)
    reserved = Relationship('Accommodation', 'RESERVED')
    reviewed = Relationship('Accommodation', 'REVIEWED', model=ReviewRel)

class Accommodation(StructuredNode):
    accomodation_id= StringProperty(required=True)
    is_reserved = Relationship('User', 'RESERVED_BY')
    is_reviewed = Relationship('User', 'IS_REVIEWED', model=ReviewRel)
    
