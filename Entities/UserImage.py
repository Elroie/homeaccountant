import datetime
from mongoengine import *
from Entities.User import User


class UserImage(Document):
    id = UUIDField(required=True, primary_key=True)
    user_id = UUIDField(required=True)
    name = StringField()
    unique_id = StringField()
    image = ImageField()
    price = FloatField()
    from_date = DateTimeField()
    to_date = DateTimeField()
    notes = StringField()
    classification_result = StringField()

    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(UserImage, self).save(*args, **kwargs)


