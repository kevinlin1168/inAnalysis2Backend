from params import params

class coreApis():
    def __init__(self):
        param=params()
        self.Upload = param.corehost + '/data/upload'
        self.Download = param.corehost + '/data/download'
        self.GetColumn = param.corehost + '/data/getcol' 
        self.GetFileStatus = param.corehost + '/data/getstatus'
        self.DeleteFile = param.corehost + '/data/delete'

        self.GetImg = param.corehost + '/viz/getimg'
        self.GetDataVizAlgoList = param.corehost + '/viz/data/getalgo'
        self.DoDataViz = param.corehost + '/viz/data/do'

        self.GetPreprocessAlgoList = param.corehost + '/preprocess/getalgo'
        self.doPreprocess = param.corehost + '/preprocess/do'
        self.PreviewPreprocess = param.corehost + '/preprocess/preview'
