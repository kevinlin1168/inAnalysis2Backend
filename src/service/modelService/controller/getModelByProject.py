from flask import session
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging

param=params()

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
            
            resp = []
            try:
                db=sql()
                db.cursor.execute(f"select * from model where `project_id`='{projectID}'")
                result = db.cursor.fetchall()
                data=[list(a) for a in result]
                for item in data:
                    respItem = {
                        'modelIndex': item[0],
                        'modelName': item[4],
                        'algoName': item[5]
                    }
                    resp.append(respItem)
            except Exception as e:
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.debug(f"[GetModel] resp: {resp}")
            return {"status":"success","msg":"","data":{'modelList': resp}},200


        else:
            return {"status":"error","msg":"user did not login","data":{}},401