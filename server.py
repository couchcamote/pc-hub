#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from dataclasses import dataclass
import nfc_service
import gps_service

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

@dataclass
class ReturnValue:
    balance: str
    lat: str
    lon: str
    time : str

class SetupCard(Resource):
    def get(self):
        try:
            balance = nfc_service.setup_card()
            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400 

class Reload(Resource):
    def get(self, amount):
        try:
            balance = nfc_service.reload(amount)
            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400

class Pay(Resource):
    def get(self, amount):
        try:
            balance = nfc_service.pay(amount)
            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400

class Balance(Resource):
    def get(self):
        try:
            balance = nfc_service.get_balance()
            gps_service.print_gps_data()
            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400

class Location(Resource):
    def get(self):
        try:
            packet = gps_service.get_gps_data()
            lon = gpspacket.lon
            lat = gpspacket.lat
            time = gpspacket.time
            returnvalue =  ReturnValue(str(0.0), str(lat), str(lon), str(time))  
            return returnvalue, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400            

if __name__ == '__main__':

    #Define Resource
    api.add_resource(Reload, "/reload/<float:amount>")
    api.add_resource(Pay, "/pay/<float:amount>")
    api.add_resource(Balance, "/balance")
    api.add_resource(SetupCard, "/setup")
    api.add_resource(Location, "/location")

    #Init Services
    nfc_service.init_service()

    gps_service.init_service()
    # Get Initial GPS Data
    gps_service.print_gps_data()

    app.run(host = "192.168.0.196", port = 9566, debug=True)