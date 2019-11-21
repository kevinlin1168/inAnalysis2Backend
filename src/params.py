from configparser import ConfigParser, SafeConfigParser
import os

class params():
    def __init__(self):
        config = SafeConfigParser(os.environ)
        config.read('secret.cfg')
        self.host=config.get('DEFAULT', 'host')
        self.port=int(config.get('DEFAULT', 'port'))
        self.secretKey=config.get('DEFAULT', 'secretkey')
        self.dbhost=config.get('DEFAULT', 'dbhost')
        self.dbuser=config.get('DEFAULT', 'dbuser')
        self.dbpwd=config.get('DEFAULT', 'dbpwd')
        self.dbschema=config.get('DEFAULT', 'dbschema')
        

        self.corehost=config.get('DEFAULT', 'corehost')
        self.coreport=config.get('DEFAULT', 'coreport')
        self.coreurl=self.corehost+':'+self.coreport

        self.servicepath='./src/service/'
        self.secretKey = 'iloveraid1'

        # self.dataCollectServiceRoot=self.servicepath+'dataService/'
        # self.visualizeServiceRoot=self.servicepath+'visualizeService/'

        self.dataFileTypeList={'num':['.csv'],'cv':['.zip'],'nlp':['.tsv']}
        self.projectTypeList=['abnormal', 'regression', 'classification', 'clustering']
        