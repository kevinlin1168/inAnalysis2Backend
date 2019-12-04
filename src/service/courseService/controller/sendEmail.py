from email.mime.text import MIMEText
import base64
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from flask_restful import Resource, reqparse
from params import params
from utils import tokenValidator,sql
from service.userService.utils import userUidGenerator, userSignupToken
import hashlib
import glob
import uuid
import logging
import pandas as pd

param=params()

class SendEmail(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courseID', type=str,required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.info(f'{args}')
        courseID = args['courseID']
        token = args['token']


        if tokenValidator(token):
            try:
                data=pd.read_csv('./src/student/'+courseID+'.csv')
                
                for index, row in data.iterrows():
                    studentIndex = row['StudentUID']
                    email = row[' 電子郵件']
                    # If modifying these scopes, delete the file token.pickle.
                    SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://mail.google.com/']
                    creds=None
                    if os.path.exists('google_token.pickle'):
                        with open('google_token.pickle', 'rb') as token:
                            creds = pickle.load(token)
                    if not creds or not creds.valid:
                        if creds and creds.expired and creds.refresh_token:
                            creds.refresh(Request())
                        else:
                            flow = InstalledAppFlow.from_client_secrets_file(
                                'client_secret.json', SCOPES)
                            creds = flow.run_local_server(port=0)
                        # Save the credentials for the next run
                        with open('google_token.pickle', 'wb') as token:
                            pickle.dump(creds, token)
                    service = build('gmail', 'v1', credentials=creds)
                    url = f"{param.frontendurl}/#/judge/{courseID}/{studentIndex}"
                    msg = MIMEText(f"<html><br>To judgement, please click the <a href={url}>url</a>.</html>",'html','utf-8')
                    msg['to'] = email
                    msg['from'] = 'inanalysis.github.io@gmail.com'
                    msg['subject'] = "Please click url to judgement"
                    raw = base64.urlsafe_b64encode(msg.as_bytes())
                    raw = raw.decode()
                    body = {'raw': raw}

                    message = (service.users().messages().send(userId="me", body=body).execute())
                return {"status": "success"}, 200


            except Exception as e:
                return {"status":"error","msg":str(e),"data":{}},400
        else:
            return {"status":"error","msg":"user did not login","data":{}},401