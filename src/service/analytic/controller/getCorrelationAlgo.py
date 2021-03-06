from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class GetCorrelationAlgoList(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetCorrelationAlgoList] args: {args}")
        token = args['token']

        #check user isLogin
        if tokenValidator(token):
            resp = requests.get(coreApi.GetCorrelationAlgoList)
            return resp.json()
        else:
            return {"status":"error","msg":"user did not login","data":{}},401