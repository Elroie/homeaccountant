from flask.json import jsonify
from mongoengine import *

from Entities.FeedNote import FeedNote
import config
import uuid
from datetime import datetime

class FeedNoteManager(object):
    def __init__(self):
        pass

    def add(self, user_id, title, text, attachment_id=None, attachment_type=None):

        connect(config.DB_NAME)

        note = FeedNote(note_id=uuid.uuid4(), user_id=user_id, text=text, title=title, time=datetime.now())

        if attachment_id is not None:
            note.attachment_id=attachment_id

        if attachment_type is not None:
            note.attachment_type=attachment_type

        note.save()
        return jsonify({'note': note.title}), 201,

    def get_all_notes(self):
        connect(config.DB_NAME)
        for note in FeedNote.objects:
            print note.title