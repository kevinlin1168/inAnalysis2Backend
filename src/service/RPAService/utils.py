from params import params
import glob
import uuid
import logging
from utils import sql

class RPAUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        while self.checkRPAID(self.uid) != ():
            self.uid=str(uuid.uuid1())

    def checkRPAID(self, userUid):
        db=sql()
        db.cursor.execute(f"select * from RPA where `RPA_id`='{self.uid}'")
        return db.cursor.fetchall()
