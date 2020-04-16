from flask_restful import Resource, reqparse
from params import params
from coreApis import coreApis
from utils import tokenValidator,sql
from threading import Thread
from service.RPAService.utils import RPAUidGenerator
from service.analytic.service.analyticService import AnalyticService
from service.file.service.fileService import FileService
from service.model.service.modelService import ModelService
import logging
import requests
import json
import time

param=params()

class RunRPA(Resource):
    def __init__(self):
        self.nodes = []
        self.links = []
        self.project = {}
        self.dataObj = {}
        self.threadsCount = 0
        self.finishCount = 0
        self.RPAID = ''
        self.token = ''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userID', type=str, required=True)
        parser.add_argument('projectID', type=str, required=True)
        parser.add_argument('token',type=str,required=True)
        args = parser.parse_args()
        logging.debug(f"[runRPA] args: {args}")

        userID = args['userID']
        projectID = args['projectID']
        token = args['token']
        self.token = token

        if tokenValidator(token):
            try:
                db=sql()
                db.cursor.execute(f"select RPA_id from RPA where `project_id`='{projectID}' and `user_id` = '{userID}' and `top_version` = 'Y'")
                result,  = db.cursor.fetchone()
                logging.debug(f"[runRPA] result: {result}")
                RPAID = result
                self.RPAID = RPAID
                with open(param.RPAFilepath + '\\'+ result + '.json') as json_file:
                    data = json_file.read()
                jsonObj = json.loads(data)
                self.project = json.loads(json.loads(jsonObj["project"]))
                jsonObj['status'] = 'processing'
                self.dataObj = jsonObj
                # logging.debug(f'{project}')
                self.nodes = self.dataObj["nodes"]
                self.links = self.dataObj["links"]
                if(self.nodes == [] or self.links == []):
                    self.dataObj['status'] = 'success'
                self.saveFile()
                fileNodeList = list(filter(lambda x: x['type'] == 'File', self.nodes))
                threads = []
                self.threadsCount = len(fileNodeList)
                for index, fileNode in enumerate(fileNodeList):
                    logging.debug('thread')
                    # self.runFlow(fileNode["id"])
                    threads.append(Thread(target = self.runFlow, args = (fileNode["id"],True)))
                    # threads.append(RPA(fileNode["id"]))
                    threads[index].start()
                return {"status":"success", "msg": "Run RPA success", "data": {}}, 200
            except Exception as e:
                self.dataObj['status'] = 'error'
                self.saveFile()
                logging.debug(f"[runRPA] error: {e}")
                return {"status":"error","msg":f"Run RPA Error: {e}","data":{}},200
                db.conn.rollback()
            finally:
                db.conn.close()  
                

        else:
            return {"status":"error","msg":"user did not login","data":{}},401

    def findLinkNode(self, id, NodeList, linkList):
        linkedNodeList = []
        linkList = filter(lambda x: x['from'] == id, linkList)
        for link in linkList:
            nodes = filter(lambda x: x['id'] == link['to'], NodeList)
            for node in nodes:
                # logging.debug(f'node: {node}')
                linkedNodeList.append(node)
        return linkedNodeList

    def updateLinkFileID(self, id, fileID, NodeList, linkList):
        LinkNodeList = self.findLinkNode(id, NodeList, linkList)
        for linkNode in LinkNodeList:
            index = next((i for i in range(len(self.nodes)) if self.nodes[i]['id'] == linkNode['id']), None)
            self.nodes[index]['attribute']['newFileID'] = fileID
    
    def updateLinkModelID(self, id, modelID, NodeList, linkList):
        LinkNodeList = self.findLinkNode(id, NodeList, linkList)
        for linkNode in LinkNodeList:
            index = next((i for i in range(len(self.nodes)) if self.nodes[i]['id'] == linkNode['id']), None)
            self.nodes[index]['attribute']['modelID'] = modelID

    def runFlow(self, id, isRoot = False):
        try:
            LinkNodeList = self.findLinkNode(id, self.nodes, self.links)
            for linkNode in LinkNodeList:
                nodeType = linkNode['type']
                attribute = linkNode['attribute']
                if(nodeType == 'Preprocessing'):
                    logging.debug(f'{attribute}')
                    if 'newFileID' in attribute:
                        logging.debug('Delete New File')
                        response = FileService().deleteFile(self.token, attribute['newFileID'])
                        if(response['status'] != 'success'):
                            raise Exception('Delete New File Error')
                    logging.debug(f'doPreprocessing')
                    response = AnalyticService().doPreprocess(self.token, attribute['fileID'], attribute['action'])
                    logging.debug(f'response: {response}')
                    if(response['status'] == 'success'):
                        index = next((i for i in range(len(self.nodes)) if self.nodes[i]['id'] == linkNode['id']), None)
                        self.nodes[index]['attribute']['newFileID'] = response['data']['fileUid']
                        self.updateLinkFileID(linkNode['id'], response['data']['fileUid'], self.nodes, self.links)
                        self.saveFile()
                        self.runFlow(linkNode['id'])
                    else:
                        raise Exception('doPreprocessingError')
                elif (nodeType == 'Model'):
                    if 'modelID' in attribute:
                        logging.debug('Delete Model')
                        status, response = ModelService().deleteModel(attribute['modelID'], self.token)
                        if(response['status'] != 'success'):
                            raise Exception('Delete Model Error')
                    response = AnalyticService().doModelTrain(self.token, attribute['newFileID'], self.project['dataType'], self.project['projectType'], attribute['algoName'], attribute['param'], attribute['input'], attribute['output'])
                    if(response['status'] == 'success'):
                        index = next((i for i in range(len(self.nodes)) if self.nodes[i]['id'] == linkNode['id']), None)
                        self.nodes[index]['attribute']['modelID'] = response['data']['modelUid']
                        self.updateLinkModelID(linkNode['id'], response['data']['modelUid'], self.nodes, self.links)
                        self.saveFile()
                        self.runFlow(linkNode['id'])
                    else:
                        raise Exception('doModelTrainError')
                elif (nodeType == 'Predict' or nodeType == 'Test'):
                    logging.debug(f'nodeType:{nodeType}')
                    if ('modelID' in attribute) and ('newFileID' in attribute):
                        response = ModelService().getModelStatus(self.token, attribute['modelID'])
                        while(response['data'] != 'success'):
                            logging.debug(f'response{response}')
                            if(response['data'] == 'fail'):
                                raise Exception('Train Model fail')
                            time.sleep(180)
                            response = ModelService().getModelStatus(self.token, attribute['modelID'])
                        if(nodeType == 'Predict'):
                            if 'predictFileID' in attribute:
                                logging.debug('Delete Predict File')
                                response = FileService().deleteFile(self.token, attribute['predictFileID'])
                                if(response['status'] != 'success'):
                                    raise Exception('Delete Predict File Error')
                            response = AnalyticService().doModelPredict(self.token, attribute['modelID'], attribute['newFileID'], '0')
                            if(response['status'] == 'success'):
                                index = next((i for i in range(len(self.nodes)) if self.nodes[i]['id'] == linkNode['id']), None)
                                self.nodes[index]['attribute']['predictFileID'] = response["data"]["predictedFileUid"]
                                self.nodes[index]['isComplete'] = True
                                self.saveFile()
                                self.runFlow(linkNode['id'])
                        if(nodeType == 'Test'):
                            response = AnalyticService().doModelTest(self.token, attribute['modelID'], attribute['newFileID'], '')
                            if(response['status'] == 'success'):
                                index = next((i for i in range(len(self.nodes)) if self.nodes[i]['id'] == linkNode['id']), None)
                                self.nodes[index]['attribute']['testResp'] = response["data"]
                                self.nodes[index]['isComplete'] = True
                                self.saveFile()
                                self.runFlow(linkNode['id'])
            if(isRoot == True):
                self.finishCount = self.finishCount + 1
                if(self.finishCount == self.threadsCount):
                    logging.debug('finish')
                    self.dataObj['status'] = 'success'
                    self.saveFile()
        except Exception as e:
            # self.dataObj['status'] = 'error'
            self.saveFile()
    
    def saveFile(self):
        try:
            self.dataObj['nodes'] = self.nodes
            with open(param.RPAFilepath + '\\'+ self.RPAID + '.json', 'w') as json_file:
                json_file.write(json.dumps(self.dataObj))
        except Exception as e:
            raise Exception(f'[runRPA]{e}')
    