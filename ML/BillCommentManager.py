from flask.json import jsonify
from mongoengine import *

from Entities.BillComment import BillComment
import config
import uuid
from datetime import datetime

class BillCommentManager(object):
    def __init__(self):
        pass

    def add(self, user_id, bill_id, text):

        connect(config.DB_NAME)

        comment = BillComment(id=uuid.uuid4(), user_id=user_id, bill_id=bill_id,text=text, time=datetime.now())
        comment.save()
        return jsonify({'note': comment.text}), 201,

    def get_all_comments(self,user_id,bill_id):
        connect(config.DB_NAME)
        return BillComment.objects(user_id=user_id , bill_id = bill_id)

    def bill_comments_count(self,user_id,bill_id):
        connect(config.DB_NAME)
        return len(BillComment.objects(user_id=user_id , bill_id = bill_id))