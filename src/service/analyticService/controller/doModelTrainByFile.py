from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class DoModelTrain(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('FileIndex', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        parser.add_argument('dataType', type=str, required=True)
        parser.add_argument('projectType', type=str, required=True)
        parser.add_argument('algoName', type=str, required=True)
        parser.add_argument('param', type=str, required=True)
        parser.add_argument('input', type=str, required=True)
        parser.add_argument('output', type=str, required=True)
        args = parser.parse_args()
        logging.debug(f"[DoModelTrain] args: {args}")

        FileIndex = args['FileIndex']
        token = args['token']
        dataType = args['dataType']
        projectType = args['projectType']
        algoName = args['algoName']
        param = args['param']
        inputColumn = args['input']
        output = args['output']

        #check user isLogin
        if tokenValidator(token):
            try:
                form = {
                    'token': token,
                    'fileUid': FileIndex,
                    'dataType': dataType,
                    'projectType': projectType,
                    'algoName': algoName,
                    'param': param,
                    'input': inputColumn,
                    'output': output
                }            
                resp = requests.post(coreApi.DoModelTrain, data=form)
                response = resp.json()
                if response['status'] == 'success':
                    try:
                        return response, 200
                    except Exception as e:
                        logging.error(str(e))
                        db.conn.rollback()
                else: 
                    return {"status":"error","msg":response['msg'],"data":{}},500
            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":f"{str(e)}","data":{}},500
                db.conn.rollback()
            finally:
                db.conn.close()
            
        else:
            return {"status":"error","msg":"user did not login","data":{}},401