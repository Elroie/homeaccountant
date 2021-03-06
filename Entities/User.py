import uuid
from config import Config
from mongoengine import *
from passlib.apps import custom_app_context as pwd_context
# from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from itsdangerous import TimedSerializer, BadSignature, SignatureExpired
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import config


class User(Document):
    id = UUIDField(required=True, primary_key=True)
    username = StringField(required=True)
    password = StringField(required=True)
    firstName = StringField(required=True)
    lastName = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    country = StringField(required=True)
    city = StringField(required=True)
    address = StringField(required=True)
    homeType = StringField(required=True)
    homeSize = IntField(required=True)
    income = IntField(required=True)
    residence = StringField(required=True)

    @staticmethod
    def hash_password(password):
        password = pwd_context.encrypt(password)
        return password

    def verify_hashed_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=9000000):
        s = TimedSerializer(Config.SECRET_KEY)
        return s.dumps({'id': str(self.id)})

    @staticmethod
    def verify_auth_token(token):
        s = TimedSerializer(Config.SECRET_KEY)
        try:
            data = s.loads(token, max_age=9000000)
        except SignatureExpired:
            # valid token, but expired
            # todo:omri you should check why this is expire so fast....
            print 'expired but still a valid token continuing....'
        except BadSignature:
            return None # invalid token
        id = uuid.UUID(data['id'])
        user = User.objects(id=id).first()
        return user
