
from flask import Flask
from flask_restful import Api, Resource, reqparse
import nfc_service


app = Flask(__name__)
api = Api(app)

@dataclass
class ReturnValue:
    balance: float
    lat: float
    lon: int
    time : str

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

api.add_resource(Reload, "/reload/<string:amount>")
api.add_resource(Pay, "/pay/<string:amount>")
api.add_resource(Balance, "/balance")

app.run (host = "localhost", port = 9566, debug=True)
app.run()