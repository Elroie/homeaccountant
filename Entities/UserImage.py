from mongoengine import *
from Entities.User import User


class UserImage(Document):
    id = UUIDField(required=True, primary_key=True)
    user = ReferenceField(User)
    name = StringField()
    image = ImageField()
    classification_result = StringField()

