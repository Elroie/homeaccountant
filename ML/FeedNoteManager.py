from mongoengine import *

from Entities.User import User
from Entities.FeedNote import FeedNote
import config
import uuid
from datetime import datetime


class FeedNoteManager(object):

    def add(self, user_id, title, text, attachment_id=None, attachment_type=None):
        connect(config.DB_NAME)

        note = FeedNote(note_id=uuid.uuid4(), user_id=user_id, text=text, title=title, time=datetime.now())

        if attachment_id is not None:
            note.attachment_id = attachment_id

        if attachment_type is not None:
            note.attachment_type = attachment_type

        note.save()

    def get_all_notes(self, user_id):
        connect(config.DB_NAME)
        notes = FeedNote.objects(user_id=user_id)
        return notes

    def get_note_count(self,user_id):
        connect(config.DB_NAME)
        return len(FeedNote.objects(user_id=user_id))

