from neomodel import (StructuredNode, StringProperty, ArrayProperty,
                      BooleanProperty,IntegerProperty,RelationshipTo)   

class Accommodation(StructuredNode):
    id= StringProperty(required=True)
    host_id= StringProperty()
    name= StringProperty()
    location= StringProperty()
    features=ArrayProperty(StringProperty())
    image_urls= ArrayProperty(StringProperty())
    min_guests= IntegerProperty()
    max_guests= IntegerProperty()
    auto_accept_flag= BooleanProperty()
    was_reserved = RelationshipTo('User', 'WAS_RESERVED')
    