from flask import session
from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class GetModelByProjectID(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetModel] args: {args}")

        projectID = args['projectID']

        #check user isLogin
        if tokenValidator(args['token']):
            
            respList = []
            try:
                db=sql()
                db.cursor.execute(f"select * from model where `project_id`='{projectID}'")
                result = db.cursor.fetchall()
                data=[list(a) for a in result]
                for item in data:
                    if item[1] == None:
                        respItem = {
                            'modelIndex': item[0],
                            'fileID': item[4],
                            'modelName': item[5],
                            'algoName': item[6]
                        }
                        respList.append(respItem)
                    else:
                        form = {
                            "token": args['token'],
                            "modelUid": item[1]
                        }
                        resp = requests.get( coreApi.GetModelStatus, data= form)
                        response = resp.json()
                        if(response['status'] == 'success'):
                            respItem = {
                                'modelIndex': item[0],
                                'status': response['data'],
                                'fileID': item[4],
                                'modelName': item[5],
                                'algoName': item[6]
                            }
                            respList.append(respItem)
                        else:
                            return {"status":"fail","msg":"get model status error","data":{}},500
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.debug(f"[GetModel] resp: {respList}")
            return {"status":"success","msg":"","data":{'modelList': respList}},200


        else:
            return {"status":"error","msg":"user did not login","data":{}},401