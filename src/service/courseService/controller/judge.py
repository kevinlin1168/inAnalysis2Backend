from flask import session
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
import logging
import json

param=params()

class Judge(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('judgeID',type=str,required=True)
        parser.add_argument('courseID',type=str,required=True)
        parser.add_argument('submitList',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[Judge] args: {args}")

        judgeID = args['judgeID']
        courseID = args['courseID']
        judgeList = json.loads(args['submitList'])

        try:
            for judge in judgeList:
                db=sql()
                db.cursor.execute(f"update score set `score`='{judge['score']}' where `course_id`='{courseID}' AND `judge_id` = '{judgeID}' AND `student_id` = '{judge['id']}'")
            db.conn.commit()

        except Exception as e:
            db.conn.rollback()
        finally:
            db.conn.close()
        return {"status":"success","msg":"Judge success","data":''},200
