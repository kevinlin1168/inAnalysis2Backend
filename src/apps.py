import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from service.systemService.controller.getDataProject import GetDataProject
from service.systemService.controller.getDataFile import GetDataFile
from service.userService.controller.signin import Singin
from service.userService.controller.signup import Singup
from service.userService.controller.signupVerify import SingupVerify
from service.userService.controller.generateToken import GenerateToken
from service.userService.controller.getUserInfo import GetUserInfo
from service.userService.controller.forgetPassword import ForgetPassword
from service.userService.controller.forgetPasswordVerify import ForgetPasswordVerify
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
from service.analyticService.controller.getCorrelationAlgo import GetCorrelationAlgoList
from service.analyticService.controller.doPreprocess import DoPreprocess
from service.analyticService.controller.doCorrelation import DoCorrelation
from service.analyticService.controller.previewPreprocess import PreviewPreprocess
from service.analyticService.controller.getAnalyticAlgoByProject import GetAnalyticsAlgoByProject
from service.analyticService.controller.getAnalyticAlgoParam import GetAnalyticAlgoParam
from service.analyticService.controller.doModelTrain import DoModelTrain
from service.analyticService.controller.doModelTrainByFile import DoModelTrainByFile
from service.analyticService.controller.getModelPreview import GetModelPreview
from service.analyticService.controller.doModelTest import DoModelTest
from service.analyticService.controller.doModelPredict import DoModelPredict
from service.analyticService.controller.stopTraining import StopTraining
from service.analyticService.controller.getModelParameter import GetModelParameter
from service.modelService.controller.addModel import AddModel
from service.modelService.controller.getModelByProject import GetModelByProjectID
from service.modelService.controller.deleteModel import DeleteModel
from service.courseService.controller.addCourse import AddCourse
from service.courseService.controller.uploadStudentFile import UploadStudentFile
from service.courseService.controller.getCourse import GetCourse
from service.courseService.controller.deleteCourse import DeleteCourse
from service.courseService.controller.getCourseByID import GetCourseByID
from service.courseService.controller.modifyCourse import ModifyCourse
from service.courseService.controller.getStudent import GetStudent
from service.courseService.controller.judge import Judge
from service.courseService.controller.sendEmail import SendEmail
from service.RPAService.controller.saveRPA import saveRPA
from service.RPAService.controller.loadRPA import loadRPA
from service.RPAService.controller.exportRPA import exportRPA
from datetime import timedelta
import logging
import sys
sys.dont_write_bytecode = True #disable __pycache__
from params import params

param=params()
app = Flask(__name__)
app.config['SECRET_KEY'] = param.secretKey
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
api = Api(app)
cors = CORS(app)

# bind api
api.add_resource(GetDataProject, "/system/getDataProject")
api.add_resource(GetDataFile, "/system/getDataFile")

api.add_resource(Singin, "/user/signin")
api.add_resource(Singup, "/user/signup")
api.add_resource(SingupVerify, "/user/signupVerify")
api.add_resource(GenerateToken, "/user/generateToken")
api.add_resource(GetUserInfo, "/user/getUserInfo")
api.add_resource(ForgetPassword, "/user/forgetPassword")
api.add_resource(ForgetPasswordVerify, "/user/forgetPasswordVerify")

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
api.add_resource(GetCorrelationAlgoList, '/analytic/getCorrelationAlgo')
api.add_resource(DoPreprocess, '/analytic/doPreprocess')
api.add_resource(DoCorrelation, '/analytic/doCorrelation')
api.add_resource(PreviewPreprocess, '/analytic/preprocessPreview')
api.add_resource(GetAnalyticsAlgoByProject, '/analytic/getAnalyticsAlgoByProject')
api.add_resource(GetAnalyticAlgoParam, '/analytic/getAnalyticAlgoParam')
api.add_resource(DoModelTrain, '/analytic/doModelTrain')
api.add_resource(DoModelTrainByFile, '/analytic/doModelTrainByFile')
api.add_resource(DoModelTest, '/analytic/doModelTest')
api.add_resource(GetModelPreview, '/analytic/getModelPreview')
api.add_resource(DoModelPredict, '/analytic/doModelPredict')
api.add_resource(StopTraining, '/analytic/stopModelTraining')
api.add_resource(GetModelParameter, '/analytic/getModelParameter')

api.add_resource(AddModel, '/model/addModel')
api.add_resource(GetModelByProjectID, '/model/getModelByProjectID')
api.add_resource(DeleteModel, '/model/deleteModel')

# Api for RPA
api.add_resource(saveRPA, '/RPA/saveRPA')
api.add_resource(loadRPA, '/RPA/loadRPA')
api.add_resource(exportRPA, '/RPA/exportRPA')

# Api for TA
api.add_resource(UploadStudentFile, '/course/uploadStudentFile')
api.add_resource(AddCourse, '/course/addCourse')
api.add_resource(GetCourse, '/course/getCourse')
api.add_resource(DeleteCourse, '/course/deleteCourse')
api.add_resource(GetCourseByID, '/course/getCourseByID')
api.add_resource(ModifyCourse, '/course/modifyCourse')
api.add_resource(GetStudent, '/course/getStudent')
api.add_resource(Judge, '/course/studentJudge')
api.add_resource(SendEmail, '/course/sendEmail')

if __name__ == "__main__":
    if '--debug' in sys.argv:
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO , format='[%(levelname)s] %(message)s')
    logging.info(f'Inanalysis running at port {param.port}')
    app.run(debug='--debug' in sys.argv,port=param.port,host=param.host)
