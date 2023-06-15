from neomodel import (StructuredNode, StringProperty,RelationshipTo)


class User(StructuredNode):
    id = StringProperty(unique_index=True, required=True)
    first_name=StringProperty()
    last_name= StringProperty()
    home_address= StringProperty()
    gender= StringProperty()
    reserved = RelationshipTo('Accommodation', 'RESERVED')
