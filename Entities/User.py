from mongoengine import *


class User(Document):
    id = UUIDField(required=True, primary_key=True)
    username = StringField(required=True)
    password = StringField(required=True)
    # images = ListField(EmbeddedDocumentField('UserImage'))
