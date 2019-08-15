from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator,sql
import hashlib
import glob
import uuid
import logging

# app = Flask(__name__)
# api = Api(app)

param=params()

class Singin(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('account', type=str,required=True)
            parser.add_argument('password',type=str,required=True)
            # parser.add_argument('user',type=str,required=True)
            args = parser.parse_args()

            md5 = hashlib.md5()
            md5.update(args['password'].encode("utf-8"))

            password = md5.hexdigest()
            try:
                db=sql()
                db.cursor.execute(f"select * from user where `user_account`='{args['account']}' AND `user_password`='{password}'")
                result = db.cursor.fetchall()
                logging.info(f'Search result {result}')

                if result != () :
                    return {"status":"success","msg":"","data":{"token":password}},200
                else:
                    return {"status":"success","msg":"user don't exist"},200

            except Exception as e:
                db.conn.rollback()
            finally:
                db.conn.close()

        except Exception as e:
            return {"status":"error","msg":f"login error:{e}","data":{}},400