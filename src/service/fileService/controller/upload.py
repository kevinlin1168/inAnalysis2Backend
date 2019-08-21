from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator,sql
import requests
import glob
import logging

# app = Flask(__name__)
# api = Api(app)

param=params()

class Upload(Resource):
    def post(self):
        fName='[Upload]'
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files',required=True)
        parser.add_argument('type',type=str,required=True)
        parser.add_argument('userID',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[Upload] args: {args}")
        file = args['file']
        dataType=args['type']
        userID=args['userID']

        #check user isLogin
        if getUserStatus.checkUserStatus(userID):

            pft=param.dataFileType
            #check project type
            if dataType not in pft:
                return {"status":"error","msg":"project type not supported","data":{}},400
            
            #check filetype
            
            filename=file.filename
            filetype=filename[filename.rfind("."):]
            logging.debug(f"[Upload] File type:{filetype}")
            if filetype not in pft[dataType]:
                return {"status":"error","msg":"file type error","data":{}},400

            data = {
                'file': file,
                'type': dataType,
                'tokenstr': 'test',
                'tokenint': 123
            }

            #todo change ip
            resp = requests.post( param.corehost + '/data/upload', data = data)

            logging.info(f'{resp}')

            # try:
            #     db=sql()
            #     db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`) values ('{uid}','{dataType}','{savedPath}','{numFilePath}',False);")
            #     db.conn.commit()
            # except Exception as e:
            #     db.conn.rollback()
            # finally:
            #     db.conn.close()
            # logging.info(f"[Upload] OK with file uid {uid}")
            # return {"status":"success","msg":"","data":{"fileUid":uid}},201
        
        else:
            return {"status":"error","msg":"user did not login","data":{}},401