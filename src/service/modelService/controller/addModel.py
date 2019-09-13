from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
from service.modelService.utils import modelIndexGenerator
import glob
import logging

param=params()

class AddModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('projectID', type=str,required=True)
        parser.add_argument('userID', type=str,required=True)
        parser.add_argument('fileID', type=str,required=True)
        parser.add_argument('modelName',type=str,required=True)
        parser.add_argument('token',type=str,required=False)
        args = parser.parse_args()
        logging.info(f'[AddModel] {args}')


        projectID = args['projectID']
        fileID = args['fileID']
        modelName = args['modelName']
        userID = args['userID']
        token = args['token']
        
        #check user isLogin
        if tokenValidator(token):
            index = modelIndexGenerator().index
            try:
                db=sql()
                db.cursor.execute(f"insert into model (`model_index`,`user_id`,`project_id`,`file_id`,`model_name`) values ('{index}','{userID}','{projectID}','{fileID}','{modelName}');")
                db.conn.commit()
                return {"status":"success","msg":"","data":{"modelID":index}},201

            except Exception as e:
                return {"status":"error","msg":str(e),"data":{}},400
            finally:
                db.conn.close()


        else:
            return {"status":"error","msg":"user did not login","data":{}},401    

