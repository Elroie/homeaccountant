from flask.json import jsonify
from mongoengine import *

from Entities.BillComment import BillComment
import config
import uuid
from datetime import datetime

from Entities.GraphData import GraphData


class GraphDataManager(object):
    def __init__(self):
        pass

    def add(self, user_id, is_forecast=False, month=5, electricity_price=0, water_price=0,other_price=0):

        connect(config.DB_NAME)
        graphdata = GraphData(id=uuid.uuid4(), user_id=user_id,is_forecast=is_forecast, month=month, electricity_price=electricity_price, water_price=water_price, other_price=other_price)
        graphdata.save()
        return jsonify({'total': electricity_price+water_price+other_price}), 201,

    def get_all_graphdata(self,user_id):
        connect(config.DB_NAME)
        # return list(FeedNote.objects(user_id=uuid.UUID(user_id)))
        # return list(FeedNote.objects(user_id=user_id))
        #user =  User.objects(id=uuid.UUID(user_id)).first()
        graphdata = GraphData.objects(user_id=user_id)
        return graphdata