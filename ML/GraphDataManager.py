import collections

import numpy
from flask.json import jsonify
from mongoengine import *

from Entities.BillComment import BillComment
import config
import uuid
import pandas
from datetime import datetime
import requests
from sklearn import linear_model
from Entities.GraphData import GraphData


class GraphDataManager(object):
    def __init__(self):
        pass

    def init_Data_DB(self,user_id):
        connect(config.DB_NAME)
        count = len(GraphData.objects())
        if 12 > count:
            GraphData.drop_collection()
            len(GraphData.objects())
            for x in range(1, 13):
                self.add(user_id, x , 0 , 0 , 0)
        else:
            print("Graph DB is OK")
        return 200

    def add(self, user_id, month, electricity_price=0, water_price=0,other_price=0):
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
        records_count = 0
        for data in graphdata:
            if data.electricity_price + data.water_price + data.other_price > 0:
                total += data.electricity_price + data.water_price + data.other_price
                records_count += 1
        if total != 0:
            return (total/records_count + abs(round((25-(self.get_future_temp(month)[0]))*500)))
        else:
            return 0

    def get_detailed_forecast(self, month):
        graphdata = GraphData.objects()
        total_electricity = 0
        total_water = 0
        total_other = 0
        records_count=0
        addition = abs(round((25 - (self.get_future_temp(month)[0])) * 5gi00))
        for data in graphdata:
            if data.electricity_price + data.water_price + data.other_price > 0:
                total_electricity += data.electricity_price
                total_water += data.water_price
                total_other += data.other_price
                records_count +=1
        empty_record = {
            'electricity_price': total_electricity/records_count+addition,
            'water_price': total_water/records_count+addition,
            'other_price': total_other/records_count+addition,
            'month': str(month)
        }
        return empty_record

    def get_future_temp(selfself, month):
        historical = collections.OrderedDict({
            '1/1/2014': 17.9,
            '2/1/2014': 17,
            '3/1/2014': 20.6,
            '4/1/2014': 23,
            '5/1/2014': 26.1,
            '6/1/2014': 27.5,
            '7/1/2014': 29.4,
            '8/1/2014': 30.2,
            '9/1/2014': 29.4,
            '10/1/2014': 27.3,
            '11/1/2014': 23.4,
            '12/1/2014': 19.2,
            '1/1/2015': 17.9,
            '2/1/2015': 17,
            '3/1/2015': 20.6,
            '4/1/2015': 23,
            '5/1/2015': 26.1,
            '6/1/2015' : 27.5,
            '7/1/2015' : 29.4,
            '8/1/2015' : 30.2,
            '9/1/2015' : 29.4,
            '10/1/2015' : 27.3,
            '11/1/2015' : 23.4,
            '12/1/2015' : 19.2,
            '1/1/2016' : 17.5,
            '2/1/2016' : 17.7,
            '3/1/2016' : 19.2,
            '4/1/2016' : 22.8,
            '5/1/2016' : 24.9,
            '6/1/2016' : 28,
            '7/1/2016' : 29.6,
            '8/1/2016' : 30,
            '9/1/2016' : 30.1,
            '10/1/2016' : 27.6,
            '11/1/2016' : 23.6,
            '12/1/2016' : 20,
            '1/1/2017' : 17.4,
            '2/1/2017' : 17.2,
            '3/1/2017' : 19.6,
            '4/1/2017' : 23,
            '5/1/2017' : 26})
        new = []
        for key in historical.keys():
            new.append((datetime.strptime(key, '%m/%d/%Y') - datetime.strptime('1/1/2014', '%m/%d/%Y')).days)
        new.sort()
        df = pandas.DataFrame(historical.values(), index=historical.keys(),columns=['temp'])
        # df = pandas.DataFrame.from_dict(historical)
        x = numpy.array(new).reshape((len(new), 1))
        y = numpy.array(df['temp'].values)
        ln = linear_model.LinearRegression()
        ln.fit(x,y)
        #print("date : temp : predict")
        # for key in historical.keys():
        #     print(key + " : " + str(historical[key]) + " : " + str(ln.predict(numpy.array((datetime.strptime(key, '%m/%d/%Y') - datetime.strptime('1/1/2014', '%m/%d/%Y')).days))))
        return ln.predict(numpy.array((datetime.strptime(str(month)+'/1/2017', '%m/%d/%Y') - datetime.strptime('1/1/2014', '%m/%d/%Y')).days))

    def update_record(self, month , billtype , price):
        record = GraphData.objects(month=month).first()
        if "Electricity" in billtype:
            record.electricity_price = price
        elif "Water" in billtype:
            record.water_price = price
        else:
            record.other_price += price
        record.save()