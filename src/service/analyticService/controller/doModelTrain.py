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
        parser.add_argument('modelIndex', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        parser.add_argument('dataType', type=str, required=True)
        parser.add_argument('projectType', type=str, required=True)
        parser.add_argument('algoName', type=str, required=True)
        parser.add_argument('param', type=str, required=True)
        parser.add_argument('input', type=str, required=True)
        parser.add_argument('output', type=str, required=True)
        args = parser.parse_args()
        logging.debug(f"[DoModelTrain] args: {args}")

        modelIndex = args['modelIndex']
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
                db=sql()
                db.cursor.execute(f"select * from model where `model_index`='{modelIndex}'")
                result = db.cursor.fetchone()
                if result[4] != None:
                    # delete model
                    if result[1] != None:
                        form1 = {
                        "token": token,
                        "modelUid": result[1]
                        }
                        resp1 = requests.post(coreApi.DeleteModel, data=form1)
                        response1 = resp1.json()
                        if response1['status'] == 'success':
                            try:
                                db=sql()
                                db.cursor.execute(f"update model set `model_id`='{None}' where `model_index` = '{modelIndex}'")
                                db.conn.commit()
                            except Exception as e:
                                logging.error(str(e))
                                db.conn.rollback()
                                raise 'Delete model Error'
                        else:
                            raise 'Delete model Error'

                    form = {
                        'token': token,
                        'fileUid': result[4],
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
                            db=sql()
                            db.cursor.execute(f"update model set `model_id`='{response['data']['modelUid']}', `algo_name`='{algoName}' where `model_index`='{modelIndex}'")
                            db.conn.commit()
                            return response, 200
                        except Exception as e:
                            logging.error(str(e))
                            db.conn.rollback()
                    else: 
                        return {"status":"error","msg":"file id not found","data":{}},500
                else:
                    return {"status":"error","msg":"file id not found","data":{}},500
            except Exception as e:
                logging.error(str(e))
                return {"status":"error","msg":f"{str(e)}","data":{}},500
                db.conn.rollback()
            finally:
                db.conn.close()
            
        else:
            return {"status":"error","msg":"user did not login","data":{}},401