from params import params
from flask_restful import Resource, reqparse
from flask import session
import logging

param=params()

class GetUserStatus:
    def checkUserStatus(self, sessionKey):
        if session.get(sessionKey) != None:
            return True
        else:
            return False
    