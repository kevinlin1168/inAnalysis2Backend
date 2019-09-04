from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
import logging
import requests

param=params()
coreApi=coreApis()

class DeleteModel(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('modelIndex', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[DeleteModel] args: {args}")

        modelIndex = args['modelIndex']
        token = args['token']

        #check user isLogin
        if tokenValidator(args['token']):
            try:
                db=sql()
                db.cursor.execute(f"select * from model where `model_index`='{modelIndex}'")
                result = db.cursor.fetchone()
                if(result[1] != None):
                    form = {
                        'fileUid': result[1],
                        'token': token
                    }
                    response = requests.post( coreApi.DeleteFile, data= form)
                    responseObj = response.json()
                    if responseObj["status"] == "success":
                        logging.info('success')
                        db.cursor.execute(f"delete from model where `model_index` = '{modelIndex}'")
                        db.conn.commit()
                        logging.info(f"[DeleteModel] OK with file id {modelIndex}")
                        return {"status":"success","msg":"","data":{}},200
                    else:
                        return responseObj
                else:
                    db.cursor.execute(f"delete from model where `model_index` = '{modelIndex}'")
                    db.conn.commit()
                    logging.info(f"[DeleteModel] OK with file id {modelIndex}")
                    return {"status":"success","msg":"","data":{}},200

                
            except Exception as e:
                logging.error(str(e))
                db.conn.rollback()
            finally:
                db.conn.close()


        else:
            return {"status":"error","msg":"user did not login","data":{}},401