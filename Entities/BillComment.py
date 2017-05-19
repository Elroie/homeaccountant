from mongoengine import *
from Entities.User import User
from Entities.ScannedImage import ScannedImage

class BillComment(Document):
    user_id = UUIDField(required=True)
    bill_id = UUIDField(required=True)
    id = UUIDField(required=True, primary_key=True)
    text = StringField(required=True)
    time = DateTimeField(required=True)

