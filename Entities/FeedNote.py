from mongoengine import *
from Entities.User import User


class FeedNote(Document):
    user_id = UUIDField(required=True)
    note_id = UUIDField(required=True, primary_key=True)
    title = StringField(required=True)
    text = StringField(required=True)
    time = DateTimeField(required=True)
    attachment_id = StringField()
    attachment_type= StringField()

