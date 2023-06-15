from neomodel import (StructuredNode, StringProperty,Relationship,ArrayProperty,IntegerProperty,BooleanProperty)


class User(StructuredNode):
    user_id = StringProperty(unique_index=True, required=True)
    first_name=StringProperty()
    last_name= StringProperty()
    home_address= StringProperty()
    gender= StringProperty()
    reserved = Relationship('Accommodation', 'RESERVED')

class Accommodation(StructuredNode):
    accomodation_id= StringProperty(required=True)
    host_id= StringProperty()
    name= StringProperty()
    location= StringProperty()
    features=ArrayProperty(StringProperty())
    image_urls= ArrayProperty(StringProperty())
    min_guests= IntegerProperty()
    max_guests= IntegerProperty()
    auto_accept_flag= BooleanProperty()
    is_reserved = Relationship('User', 'RESERVED_BY')