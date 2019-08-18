class params():
    def __init__(self):
        self.host='140.112.26.135'
        self.port=7878

        self.servicepath='./src/service/'
        self.secretKey = 'iloveraid1'

        # self.dataCollectServiceRoot=self.servicepath+'dataService/'
        # self.visualizeServiceRoot=self.servicepath+'visualizeService/'

        self.dataFileTypeList={'num':['.csv'],'cv':['.zip'],'nlp':['.tsv']}
        self.projectTypeList=['Abnormal Detection', 'Regression', 'Classification', 'Clustering']
        self.dbhost='140.112.26.132'
        self.dbuser='ican'
        self.dbpwd='lab125a'
        self.dbschema='inanalysis'

        self.corehost='http://140.112.26.135:8787'