import time, os, sys
from time import strftime
import traceback

class Logger():

    def __init__(self, logFileName, logDir = None, debug = True):
        self.debug = debug
        self.logFP = None
        self.logFileName = logFileName
        self.format = "%Y-%m-%d_%H-%M-%S"
        if logDir == None:
            logDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("Logger.py")), os.pardir)), "logs")
        try:
            if not os.path.exists(logDir):
                os.mkdir(logDir)

            self.logFilePath = os.path.join(logDir,self.logFileName)
            self.logFP = open(self.logFilePath, "w")
        except:
            print str(sys.exc_info()[0])
            print str(sys.exc_info()[1])
            print str(traceback.extract_tb(sys.exc_info()[2]))
            raise
            
    def getLogFilePath(self):
        return self.logFilePath
    
    def Log(self, *messages):        
        logMsg = strftime(self.format) + ": "
        for m in messages:
            logMsg += str(m) + " " 
        logMsg += "\n"
        if self.debug == True:
            print logMsg
        if self.logFP != None:
            self.logFP.write(logMsg)

    
    def LogWithNoTimeStamp(self, *messages):
        #logMsg = strftime(self.format) + ": "
        logMsg =  ""
        for m in messages:
            logMsg += str(m) + " "
        logMsg += "\n"
        if self.logFP != None:
            self.logFP.write(logMsg)
    
    
    def LogException(self):        
        logMsg = strftime(self.format) + ": "
        logMsg += "Exception Type: " + str(sys.exc_info()[0]) + "\n"
        logMsg += "Exception Details: " + str(sys.exc_info()[1]) + "\n"
        logMsg += "Exception Traceback: " + str(traceback.extract_tb(sys.exc_info()[2])) + "\n"
        #print logMsg
        if self.logFP != None:
            self.logFP.write(logMsg)
        return logMsg
    
    def Doc(self, *messages):        
        logMsg = ""
        for m in messages:
            logMsg += str(m) + " " 
        logMsg += "\n"
        if self.logFP != None:
            self.logFP.write(logMsg)
    
    def Critical(self, *messages):
        self.Log(*messages) 
        
    def Error(self, *messages):
        self.Log(*messages) 
        
    def Warning(self, *messages):
        self.Log(*messages) 
        
    def Info(self, *messages):
        self.Log(*messages)
        
    def Debug(self, *messages):
        self.Log(*messages) 
        
        
    def __del__(self):
        if self.logFP != None:
            self.logFP.close()
            self.logFP = None

if __name__ == "__main__":
    format = "%Y-%m-%d_%H-%M-%S"
    l = Logger(os.path.basename("Logger.py") + format.replace(".py",".txt"))
    l.Critical("Critical")
    l  = Logger(os.path.basename("Logger.py") + format.replace(".py",".txt"))    