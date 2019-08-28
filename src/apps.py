import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from service.userService.controller.signin import Singin
from service.userService.controller.signup import Singup
from service.fileService.controller.upload import Upload
from service.fileService.controller.getFileList import GetFileList
from service.fileService.controller.delete import DeleteFile
from service.fileService.controller.download import DownloadFile
from service.fileService.controller.getColumn import GetFileColumn
from service.projectService.controller.addProject import AddProject
from service.projectService.controller.getProjectByUser import GetProjectByUserID
from service.projectService.controller.deleteProject import DeleteProject
from service.visualizeService.controller.getVisAlgoList import GetVisAlgoList
from service.visualizeService.controller.dataViz import dataViz
from service.analyticService.controller.getPreprocessAlgo import GetPreprocessAlgoList
from service.analyticService.controller.doPreprocess import DoPreprocess
from datetime import timedelta
import logging
import sys
sys.dont_write_bytecode = True #disable __pycache__
from params import params

par=params()
app = Flask(__name__)
app.config['SECRET_KEY'] = par.secretKey
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
api = Api(app)
cors = CORS(app)

# bind api
api.add_resource(Singin, "/user/signin")
api.add_resource(Singup, "/user/signup")
api.add_resource(Upload, '/file/upload')
api.add_resource(GetFileList, '/file/getFileList')
api.add_resource(DeleteFile, '/file/delete')
api.add_resource(DownloadFile, '/file/download')
api.add_resource(GetFileColumn, '/file/getColumn')
api.add_resource(AddProject, '/project/add')
api.add_resource(GetProjectByUserID, '/project/getProjectByUserID')
api.add_resource(DeleteProject, '/project/delete')
api.add_resource(GetVisAlgoList, '/visualize/getAlgo')
api.add_resource(dataViz, '/visualize/doVisualize')
api.add_resource(GetPreprocessAlgoList, '/analytic/getPreprocessAlgo')
api.add_resource(DoPreprocess, '/analytic/doPreprocess')


if __name__ == "__main__":
    if '--debug' in sys.argv:
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO , format='[%(levelname)s] %(message)s')
    logging.info(f'Inanalysis running at port {par.port}')
    app.run(debug='--debug' in sys.argv,port=par.port,host='0.0.0.0')