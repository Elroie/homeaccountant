from mongoengine import *
from Entities.User import User
from Entities.ScannedImage import ScannedImage

class GraphData(Document):
    id_user = ReferenceField(User, reverse_delete_rule=CASCADE)
    id_bill = ReferenceField(ScannedImage, reverse_delete_rule=CASCADE)
    id = UUIDField(required=True, primary_key=True)
    text = StringField(required=True)
    time = StringField(required=True)

