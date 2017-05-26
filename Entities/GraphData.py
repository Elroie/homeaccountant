from mongoengine import *
from Entities.User import User
from Entities.ScannedImage import ScannedImage

class GraphData(Document):
    user_id = UUIDField(required=True)
    id = UUIDField(required=True, primary_key=True)
    month = IntField(required=True)
    electricity_price = IntField(required=True)
    water_price = IntField(required=True)
    other_price = IntField(required=True)

