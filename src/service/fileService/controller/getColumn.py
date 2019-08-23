from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests
import json

param=params()
coreApi=coreApis()

class GetFileColumn(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetFileColumn] args: {args}")

        fileID = args['fileID']

        #check user isLogin
        if tokenValidator(args['token']):
            try:
                db=sql()
                form = {
                        'fileUid': json.dump(test),
                        'tokenstr': 'ab',
                        'tokenint': 293
                    }
                logging.info(f'form:{form}')
                response = requests.post( coreApi.GetColumn, data= form)
                responseObj = response.json()
                logging.info(f'result: {responseObj}')
                return responseObj
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()


        else:
            return {"status":"error","msg":"user did not login","data":{}},401