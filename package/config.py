from os.path import dirname, abspath, join, isdir, split, isfile
from os import makedirs
import sys
import json
import logging
from logging.handlers import RotatingFileHandler
DEFAULTCONFIG = {
    "debug": False
}


class Config():

    def __init__(self):
        # initialize
        self.baseDir = dirname(dirname(abspath(sys.argv[0])))
        self.outputDir = join(self.baseDir, 'output')
        self.configDir = join(self.baseDir, 'config')
        _, self.name = split(self.baseDir)
        self.logFilePath = join(self.outputDir, self.name+'.log')
        self.debug = False
        self.loglevel = logging.INFO
        self.configJson = self.readJson('config.json')
        # update config from config.json
        self.updateConfig()

    def updateConfig(self):
        for key in self.configJson:
            if self.configJson[key] != '':
                if key in self.__dict__.keys():
                    setattr(self, key, self.configJson[key])
        del self.configJson

    def finalize(self):
        if self.debug:
            self.logFilePath = join(self.outputDir, self.name+'_debug.log')
            self.loglevel = logging.DEBUG
        self.initLogging()
        # make sure
        self.showVars()

    def makeSureDir(self, dirPath):
        if not isdir(dirPath):
            makedirs(self.outDir)

    def makeSureFile(self, filepath, text=None):
        if not isfile(filepath):
            with open(filepath, mode='w') as f:
                if text is not None:
                    f.write(text)

    def null2None(self, dict):
        for k in dict:
            if dict[k] == "":
                dict[k] = None
        return dict

    def readJson(self, fileName):
        filePath = join(self.configDir, fileName)
        try:
            self.makeSureFile(filePath,
                              json.dumps(DEFAULTCONFIG, indent=2))
            with open(filePath) as f:
                return json.load(f)
        except Exception as e:
            raise(e)

    def initLogging(self):
        # Rotate 2M * 10
        logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s',
                            level=self.loglevel,
                            datefmt='%y/%m/%d %H:%M:%S',
                            handlers=[RotatingFileHandler(
                                self.logFilePath,
                                maxBytes=2000000,
                                backupCount=10)])
        logging.addLevelName(logging.DEBUG, 'DBG')
        logging.addLevelName(logging.INFO, 'INF')
        logging.addLevelName(logging.WARNING, 'WRN')
        logging.addLevelName(logging.ERROR, 'ERR')
        logging.addLevelName(logging.CRITICAL, 'CRT')

    def showVars(self):
        print(json.dumps(self.__dict__, indent=2))
        if self.debug:
            logging.debug(json.dumps(self.__dict__, indent=2))


CONFIG = Config()
