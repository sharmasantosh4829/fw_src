import time, os, sys
from time import strftime
import threading
import thread


from SerialCommunication import *
from Trace import *

class startThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)

'''
To be used only on Windows Operating Systems
'''
class ConsoleLogger(SerialCommunication):

    def __init__(self, comPort, baudRate = 9600, prompt = None, username = None, password = None, debug = False):
        '''
        comPort has to be 'com1 or com2 etc
        '''
        self.format = "%Y-%m-%d_%H-%M-%S"
        self.baudRate = baudRate
        SerialCommunication.__init__(self, int(str(comPort).lower().strip("com")), baudRate, prompt, username, password)
        self.consoleLock = thread.allocate_lock()
        self.breakFlag = False # This is a shared variable .. guard it with consoleLock
        self.consoleProc = False
        self.logFileName = None
        self.trace = Trace("ConsoleLogger.py")
        self.log = False
        self.debug = debug
        
        
    def setLogger(self, loggerObject):
        self.log = loggerObject
        SerialCommunication.setLogger(self, self.log)
        
        
    def cLog(self, *args):
        if self.log == False:
            self.trace.Debug(*args)
            #print args
        else:
            self.log.Log(*args)
    
    
    def cLogException(self):
        if self.log == False:
            logMsg = "Exception Type: " + str(sys.exc_info()[0]) + "\n"
            logMsg += "Exception Details: " + str(sys.exc_info()[1]) + "\n"
            logMsg += "Exception Traceback: " + str(traceback.extract_tb(sys.exc_info()[2])) + "\n"
            self.trace.Debug(logMsg)
            #print logMsg
        else:
            self.log.LogException()
            
            
    def _initLogFilePath(self, logFileName = None, logDir = None):
        if self.logFileName == None:
            if logFileName == None:
                self.logFileName = "ConsoleLog-%s.txt"%strftime(self.format)
            else:
                self.logFileName = logFileName
            
            if logDir == None:
                logDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("ConsoleLogger.py")), os.pardir)), "logs")
            try:
                if not os.path.exists(logDir):
                    os.mkdir(logDir)

                self.logFilePath = os.path.join(logDir,self.logFileName)
            except:
                self.cLogException()
                raise

    def consoleThread(self):
        '''
        Private thread method .. not to be used externally
        '''
        self.connect()
        while True:
            try:
                output = self._rxStrict()
            except:
                self.cLogException()
                
            if output == None:
                output = []
            newOutput = ""
            for l in output:
                if l == '\r\n':
                    continue
                newOutput += l.strip('\r\n')
                try:
                    self.fp.write(l.strip('\r\n'))
                    self.fp.write("\n")
                except:
                    self.cLogException()
                
            try:
                #if self.debug:
                    #print "Acquiring consoleLock in consoleThread"
                self.consoleLock.acquire()
                if self.breakFlag == True:
                    try:
                        self.consoleLock.release()
                        #if self.debug:
                            #print "Released consoleLock in consoleThread"
                    except:
                        self.cLogException()
                    break
                else:
                    try:
                        self.consoleLock.release()
                        #if self.debug:
                            #print "Released consoleLock in consoleThread"
                    except:
                        self.cLogException()
            except:
                self.cLogException()
            
        try:
            self.disconnect()
        except:
            self.cLogException()
        try:
            self.fp.close()
        except:
            self.cLogException()
            
            
    def __restart(self):
        '''
        Private method .. not to be used externally
        '''
        try:
            if self.consoleProc != False:
                return
            self.fp = open(self.logFilePath, "a")
            self.consoleProc = startThread(self.consoleThread)
            self.consoleProc.start()
        except:
            self.cLogException()
            raise
        return self.logFilePath
        
    def startConsole(self, logFileName = None, logDir = None):
        '''
        Public method - to be called when the console logging should be started.
        If logFileName is not supplied a file with the time-stamped name is generated and is used to store the console logs
        If logDir is not supplied, the console log file will be stored in the "logs" folder.
        It returns the log file path.
        '''
        try:
            if self.consoleProc != False:
                self.stopConsole()
            self.logFileName = None
            self._initLogFilePath(logFileName, logDir)
            self.fp = open(self.logFilePath, "w")
            self.consoleProc = startThread(self.consoleThread)
            self.consoleProc.start()
        except:
            self.cLogException()
            raise
        return self.logFilePath

        
    def start(self, logFileName = None, logDir = None):
        '''
        Public method - to be called when the console logging should be started.
        If logFileName is not supplied a file with the time-stamped name is generated and is used to store the console logs
        If logDir is not supplied, the console log file will be stored in the "logs" folder.
        It returns the log file path.
        '''
        try:
            if self.consoleProc != False:
                self.stopConsole()
            self.logFileName = None
            self._initLogFilePath(logFileName, logDir)
            self.fp = open(self.logFilePath, "w")
            self.consoleProc = startThread(self.consoleThread)
            self.consoleProc.start()
        except:
            self.cLogException()
            raise
        return self.logFilePath
        
    
    def stopConsole(self):
        '''
        Public method - to be called when the console logging is no longer needed. It returns the console log file path
        '''
        try:
            if self.consoleProc == False:
                self.cLog("self.consoleProc is False, so stopConsole is returning early")
                return self.logFilePath
            self.cLog("Acquiring consoleLock in stopConsole")
            self.consoleLock.acquire()
            self.breakFlag = True
            self.consoleLock.release()
            self.cLog("Released consoleLock in stopConsole")
            try:
                self.consoleProc.join(60)
            except:
                pass
            self.consoleProc = False
            self.breakFlag = False
        except:
            self.cLogException()
            raise
        return self.logFilePath
        
    def stop(self):
        '''
        Public method - to be called when the console logging is no longer needed. It returns the console log file path
        '''
        try:
            if self.consoleProc == False:
                return self.logFilePath
            self.cLog("Acquiring consoleLock in stop")
            self.consoleLock.acquire()
            self.breakFlag = True
            self.consoleLock.release()
            self.cLog("Released consoleLock in stop")
            try:
                self.consoleProc.join(60)
            except:
                pass
            self.consoleProc = False
            self.breakFlag = False
        except:
            self.cLogException()
            raise
        return self.logFilePath
    
    def executeConsoleCmd(self, cmd):
        return self.execute(cmd)
        
    def execute(self, cmd):
        '''
        Public method - to be used to run non-blocking commands and also commands which do not generate a large output.
        It returns the output of the command in the form of a string (multi-line)
        '''
        try:
            self._initLogFilePath()
            self.stop()
            time.sleep(2)
            self.connect()
            time.sleep(2)
            self._tx(cmd)
            time.sleep(2)
            output = self._rxStrict()
            if output == None:
                output = []
            #time.sleep(2)
            self.disconnect()
            time.sleep(2)
            fp = open(self.logFilePath, "a")
            newOutput = ""
            for l in output:
                if l == '\r\n':
                    continue
                newOutput += l.strip('\r\n')
                try:
                    fp.write(l.strip('\r\n'))
                    fp.write("\n")
                except:
                    self.cLogException()
            fp.close()
            self.__restart()
            return newOutput
        except:
            self.cLogException()
            raise
        
    def getConsoleLogFilePath(self):
        '''
        Public method which returns the current logFilePath name
        '''
        return self.logFilePath
    

if __name__ == "__main__":
    pass