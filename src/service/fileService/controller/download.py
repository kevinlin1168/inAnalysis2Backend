from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi = coreApis()

class DownloadFile(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fileID', type=str, required=True)
        parser.add_argument('fileName', type=str, required=False)
        parser.add_argument('token', type= str, required=True)
        args = parser.parse_args()
        logging.debug(f"[DownloadFile] args: {args}")

        fileID = args['fileID']
        fileName = args['fileName']
        
    #check user isLogin
        if tokenValidator(args['token']):
            try:
                form = {
                    'fileUid': fileID,
                    'fileName': fileName
                }
                logging.info(f'form:{form}')
                resp = requests.get( coreApi.Download, data= form)
                response = resp.json()
                logging.info(f'response: {response}')
            except Exception as e:
                logging.error(str(e))


        else:
            return {"status":"error","msg":"user did not login","data":{}},401    

