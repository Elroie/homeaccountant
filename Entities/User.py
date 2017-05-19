from mongoengine import *
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import config

class User(Document):
    id = UUIDField(required=True, primary_key=True)
    username = StringField(required=True)
    password = StringField(required=True)

    @staticmethod
    def hash_password(password):
        password = pwd_context.encrypt(password)
        return password

    def verify_hashed_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })


    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    # images = ListField(EmbeddedDocumentField('UserImage'))
