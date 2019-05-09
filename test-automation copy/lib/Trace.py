import time, os, sys
from time import strftime
import logging


class Trace():

    def __init__(self, moduleName):
        self.format = "%Y-%m-%d_%H-%M-%S"
        traceDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("Trace.py")), os.pardir)), "trace")
        if not os.path.exists(traceDir):
            os.mkdir(traceDir)

        self.traceFileName = os.path.join(traceDir, os.path.basename(moduleName) + "-" + strftime(self.format) + ".tr")
        logging.basicConfig(filename = self.traceFileName, level = logging.DEBUG)

    def _createMsg(self, *messages):        
        logMsg = strftime(self.format) + ": "
        for m in messages:
            logMsg += str(m) + " " 
        #print logMsg
        return logMsg
        
    def Critical(self, *messages):
        logging.critical(self._createMsg(*messages)) 
        
    def Error(self, *messages):
        logging.error(self._createMsg(*messages)) 
        
    def Warning(self, *messages):
        logging.warning(self._createMsg(*messages))         
        
    def Info(self, *messages):
        logging.info(self._createMsg(*messages))         
        
    def Debug(self, *messages):
        logging.debug(self._createMsg(*messages))
        
