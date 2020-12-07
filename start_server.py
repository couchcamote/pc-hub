#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import json
import nfc_service
import gps_service
import config_service
import sqlitedb_service

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

@dataclass_json
@dataclass
class ReturnValue:
    balance: str
    lat: str
    lon: str
    time : str
    uid : str

class SetupCard(Resource):
    def get(self):
        try:
            balance,uid = nfc_service.setup_card()

            packet = gps_service.get_gps_data()
            lon = packet.lon
            lat = packet.lat
            time = packet.time

            gps_service.print_gps_data()

            save_transaction("TX_PAY", uid, lat, lon, balance)

            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400 

class Reload(Resource):
    def get(self, amount):
        try:
            balance,uid = nfc_service.reload(amount)

            packet = gps_service.get_gps_data()
            lon = packet.lon
            lat = packet.lat
            time = packet.time

            gps_service.print_gps_data()

            save_transaction("TX_RELOAD", uid, lat, lon, balance)

            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400

class Pay(Resource):
    def get(self, amount):
        try:
            balance,uid = nfc_service.pay(amount)

            packet = gps_service.get_gps_data()
            lon = packet.lon
            lat = packet.lat
            time = packet.time

            #gps_service.print_gps_data()

            save_transaction("TX_PAY", uid, lat, lon, balance)

            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400

class Balance(Resource):
    def get(self):
        try:
            balance,uid = nfc_service.get_balance()
            print("Card uid:", uid)

            packet = gps_service.get_gps_data()
            lon = packet.lon
            lat = packet.lat
            time = packet.time

            gps_service.print_gps_data()

            save_transaction("TX_BALANCE", uid, lat, lon, balance)

            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400

class Location(Resource):
    def get(self):
        try:
            packet = gps_service.get_gps_data()
            lon = packet.lon
            lat = packet.lat
            time = packet.time
            returnvalue =  ReturnValue(0.0, lat, lon, time,'')
            #print(returnvalue)
            #print(returnvalue.to_json())
            return json.loads(returnvalue.to_json()), 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400

class LatestTransactions(Resource):
    def get(self):
        try:
            records = sqlitedb_service.get_recent_transactions()
            return records, 200
        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400


def save_transaction(action_type, card_id, latitude, longitude, latest_balance):
    #get from device and login
    terminal = "TRM1"
    location_id = "ROUTE_LOC_01"
    driver_id = "DRV001"
    driver_name = "Sweetney Luber"

    sqlitedb_service.insert_record(terminal,action_type,card_id,latitude,longitude,location_id,latest_balance,driver_id,driver_name)

if __name__ == '__main__':

    #Define Resource
    api.add_resource(Reload, "/reload/<float:amount>")
    api.add_resource(Pay, "/pay/<float:amount>")
    api.add_resource(Balance, "/balance")
    api.add_resource(SetupCard, "/setup")
    api.add_resource(Location, "/location")
    api.add_resource(LatestTransactions, "/transactions")

    #Init Services
    nfc_service.init_service()

    gps_service.init_service()
    # Get Initial GPS Data
    gps_service.print_gps_data()

    # Get SQLite DB Service
    sqlitedb_service.init_service()

    host_confg = config_service.get_value('app','host')
    port = config_service.get_value('app','port') 
    app.run(host = '192.168.0.195', port = 9566, debug=True)
