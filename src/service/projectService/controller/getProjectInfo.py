from flask import session
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging

param=params()

class GetProjectInfo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID',type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[GetProjectInfo] args: {args}")

        projectID = args['projectID']

        #check user isLogin
        if tokenValidator(args['token']):
            
            resp = []
            try:
                db=sql()
                db.cursor.execute(f"select * from model, file where `model.project_id`='{projectID}' AND `file.project_id`='{projectID}'")
                result = db.cursor.fetchall()
                data=[list(a) for a in result]
                for item in data:
                    respItem = {
                        'projectID': item[0],
                        'projectName': item[2],
                        'projectType': item[3],
                        'dataType': item[4]
                    }
                    resp.append(respItem)
            except Exception as e:
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.debug(f"[GetProject] resp: {resp}")
            return {"status":"success","msg":"","data":{'projectList': resp}},201


        else:
            return {"status":"error","msg":"user did not login","data":{}},401