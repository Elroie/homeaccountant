from flask.json import jsonify
from mongoengine import *

from Entities.BillComment import BillComment
import config
import uuid
from datetime import datetime
import requests

from Entities.GraphData import GraphData


class GraphDataManager(object):
    def __init__(self):
        pass

    def add(self, user_id, month=5, electricity_price=0, water_price=0,other_price=0):
        connect(config.DB_NAME)
        graphdata = GraphData(id=uuid.uuid4(), user_id=user_id, month=month, electricity_price=electricity_price, water_price=water_price, other_price=other_price)
        graphdata.save()
        return jsonify({'total': electricity_price+water_price+other_price}), 201,

    def get_all_graphdata(self):
        graphdata = GraphData.objects().order_by('month')
        return graphdata

    def get_month(self,month):
        connect(config.DB_NAME)
        graphdata = GraphData.objects(month = month)
        return graphdata

    def get_temperature(self):
        appid = "242d45c54feed45b323c566056771ad3"
        city =  "294751"
        url = 'http://api.openweathermap.org/data/2.5/forecast?id='+city+'&APPID='+appid
        response = requests.get(url,verify=False)
        return response.text

    def get_forecast(self, month):
        graphdata = GraphData.objects()
        total = 0
        for data in graphdata:
            if data.electricity_price + data.water_price + data.other_price > 0:
                total += data.electricity_price + data.water_price + data.other_price
        total = total/len(graphdata)
        return total

    def get_detailed_forecast(self, month):
        graphdata = GraphData.objects()
        total_electricity = 0
        total_water = 0
        total_other = 0
        for data in graphdata:
            if data.electricity_price + data.water_price + data.other_price > 0:
                total_electricity += data.electricity_price
                total_water += data.water_price
                total_other += data.other_price
        month = datetime.now().month
        if month == 13:
            month = 1
        empty_record = {
            'electricity_price': total_electricity/len(graphdata),
            'water_price': total_water/len(graphdata),
            'other_price': total_other/len(graphdata),
            'month': str(month)
        }
        return empty_record