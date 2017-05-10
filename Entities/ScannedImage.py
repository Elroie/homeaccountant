from mongoengine import *
from Entities.UserImage import UserImage
#change the entity name to BillInfo

class ScannedImage(Document):
    original_image = ReferenceField(UserImage, reverse_delete_rule=CASCADE)
    text = MultiLineStringField()
    price = FloatField()
    from_date = DateTimeField()
    to_date = DateTimeField()
