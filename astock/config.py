import warnings
from os.path import dirname, abspath, join, isdir, split, isfile
from os import makedirs
import sys
import json
import logging
from logging.handlers import RotatingFileHandler
DEFAULTCONFIG = {
    "debug": False
}
warnings.simplefilter('ignore')


class Config():

    def __init__(self):
        # initialize
        self.baseDir = dirname(dirname(abspath(sys.argv[0])))
        self.outputDir = '/home/minato/stockData'
        self.configDir = join(self.baseDir, 'config')
        self.resourceDir = join(self.baseDir, 'resource')
        _, self.name = split(self.baseDir)
        self.debug = False
        self.configJson = self.readJson('config.json')

    def readJson(self, fileName):
        filePath = join(self.configDir, fileName)
        try:
            with open(filePath) as f:
                return json.load(f)
        except Exception as e:
            raise(e)

    def showVars(self):
        print(json.dumps(self.__dict__, indent=2))
        if self.debug:
            logging.debug(json.dumps(self.__dict__, indent=2))


CONFIG = Config()
