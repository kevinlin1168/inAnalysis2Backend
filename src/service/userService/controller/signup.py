from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from params import params
from utils import tokenValidator,sql
from service.userService.utils import userUidGenerator
import hashlib
import glob
import uuid
import logging

# app = Flask(__name__)
# api = Api(app)

param=params()

class Singup(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('account', type=str,required=True)
            parser.add_argument('name', type=str,required=True)
            parser.add_argument('password',type=str,required=True)
            parser.add_argument('email',type=str,required=False)
            args = parser.parse_args()

            db=sql()
            db.cursor.execute(f"select * from user where `user_account`='{args['account']}'")
            result = db.cursor.fetchall()

            if result == ():
                md5 = hashlib.md5()
                md5.update(args['password'].encode("utf-8"))

                password = md5.hexdigest()
                uid = userUidGenerator().uid
                try:
                    db=sql()
                    db.cursor.execute(f"insert into user (`user_id`,`user_name`,`user_account`,`user_email`,`user_password`,`user_roles`) values ('{uid}','{args['name']}','{args['account']}','{args['email']}','{password}', 1);")
                    db.conn.commit()
                    return {"status":"success","msg":"","data":{"user":uid}},201


                except Exception as e:
                    return {"status":"error","msg":str(e),"data":{}},400
                finally:
                    db.conn.close()
            else:
                return {"status":"error","msg":"account had been existed","data":{}},400

        except Exception as e:
            return {"status":"error","msg":f"signup error:{e}","data":{}},400