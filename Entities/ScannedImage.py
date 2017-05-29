import datetime
from mongoengine import *
from Entities.UserImage import UserImage
#change the entity name to BillInfo

class ScannedImage(Document):
    original_image = ReferenceField(UserImage, reverse_delete_rule=CASCADE)
    user_id = UUIDField(required=True)
    text = MultiLineStringField()
    price = FloatField()
    from_date = DateTimeField()
    to_date = DateTimeField()
    status = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(ScannedImage, self).save(*args, **kwargs)
