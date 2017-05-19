from flask.json import jsonify
from mongoengine import *

from Entities.BillComment import BillComment
import config
import uuid
from datetime import datetime

class BillCommentManager(object):
    def __init__(self):
        pass

    def add(self, user_id, title, text, attachment_id=None, attachment_type=None):

        connect(config.DB_NAME)

        note = BillComment(note_id=uuid.uuid4(), user_id=user_id, text=text, title=title, time=datetime.now())

        if attachment_id is not None:
            note.attachment_id=attachment_id

        if attachment_type is not None:
            note.attachment_type=attachment_type

        note.save()
        return jsonify({'note': note.title}), 201,

    def get_all_notes(self,user_id):
        connect(config.DB_NAME)
        return list(FeedNote.objects())

