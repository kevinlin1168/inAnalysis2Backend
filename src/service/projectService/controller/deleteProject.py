from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging

param=params()

class DeleteProject(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[DeleteProject] args: {args}")

        projectID = args['projectID']

        #check user isLogin
        if tokenValidator(args['token']):

            try:
                db=sql()
                db.cursor.execute(f"delete from project where `project_id` = '{projectID}'")
                db.conn.commit()
            except Exception as e:
                db.conn.rollback()
            finally:
                db.conn.close()
            logging.info(f"[DeleteProject] OK with project id {projectID}")
            return {"status":"success","msg":"","data":{}},201


        else:
            return {"status":"error","msg":"user did not login","data":{}},401