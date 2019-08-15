from params import params
import glob
import uuid
import logging
from utils import sql

class userUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        while self.checkUserID(self.uid) != ():
            self.uid=str(uuid.uuid1())

    def checkUserID(self, userUid):
        db=sql()
        db.cursor.execute(f"select * from user where `user_id`='{self.uid}'")
        return db.cursor.fetchall()
