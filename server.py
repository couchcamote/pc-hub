#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from dataclasses import dataclass
import nfc_service


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

@dataclass
class ReturnValue:
    balance: float
    lat: float
    lon: int
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
            return balance, 200

        except ValueError as err:
            exc = "Exception: {0}".format(str(err))
            print(err.args)
            return exc,400

api.add_resource(Reload, "/reload/<float:amount>")
api.add_resource(Pay, "/pay/<float:amount>")
api.add_resource(Balance, "/balance")
api.add_resource(SetupCard, "/setup")

app.run(host = "192.168.0.195", port = 9566, debug=True)
