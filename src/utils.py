import logging
from params import params
import pymysql
import hmac
import time  
import base64
import json

param = params()

def tokenGenerator(key = param.secretKey, expire=3600):
    timeExpire = str(time.time() + expire)  
    timeByte = timeExpire.encode("utf-8")  
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),timeByte,'sha1').hexdigest()  
    token = timeExpire+':'+sha1_tshexstr  
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))  
    return b64_token.decode("utf-8")  

def tokenValidator(token, key = param.secretKey):
    tokenDecode = base64.urlsafe_b64decode(token).decode('utf-8')  
    tokenList = tokenDecode.split(':')  
    if len(tokenList) != 2:  
        return False  
    timeExpire = tokenList[0]  
    if float(timeExpire) < time.time():  
        # token expired  
        return False  
    known_sha1_tsstr = tokenList[1]  
    sha1 = hmac.new(key.encode("utf-8"),timeExpire.encode('utf-8'),'sha1')  
    calc_sha1_tsstr = sha1.hexdigest()  
    if calc_sha1_tsstr != known_sha1_tsstr:  
        # token certification failed  
        return False  
    # token certification success  
    return True  

class sql():
    def __init__(self):
        param=params()
        self.conn=pymysql.connect(param.dbhost,param.dbuser,param.dbpwd,param.dbschema)
        self.cursor=self.conn.cursor()
