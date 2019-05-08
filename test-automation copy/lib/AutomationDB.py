import os, sys
import logging
import traceback
from time import strftime
import socket
import unittest, time, re
import string
import subprocess
import datetime
from time import strftime
import fnmatch, csv
import shutil
import traceback
from Trace import *
from Logger import *
import MySQLdb as mdb
sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("AutomationDB.py")), os.pardir)), "header"))
sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("AutomationDB.py")), os.pardir)), "lib"))
sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("AutomationDB.py")), os.pardir)), "config"))


class AutomationDB():
    
    def __init__(self,AutomationTool):
        """
        Initialization function for the Automation db
        """
        #self.mdbLog = Logger(os.path.basename("AutomationDB.py").replace(".py",".log"))
        self.mdbLog = False
        self.host = "54.183.199.137"
        self.port = 3306
        self.dataBaseName = "dev"
        self.user = "qe"
        self.password = "belkin123"
        self.dataBaseTable = AutomationTool+"_tb"
        self.trace = Trace("AutomationDB.py")
        try:
            if not os.path.exists(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("AutomationDB.py")), os.pardir)), "config", "AutomationDB.cfg")):
                raise Exception("The AutomationDB.cfg Config file does not exist in the config folder.\nPlease include the AutomationDB.cfg Config file in the config folder")
            fileReader = open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("AutomationDB.py")), os.pardir)), "config", "AutomationDB.cfg"), "r")
            lines = fileReader.readlines()
            fileReader.close()
            assert len(lines) != 0
            for line in lines:
                
                if line.find("#") == 0:
                    continue
                if line.find(AutomationTool)!=-1:
                    #print line
                    
                    self.dbQuery = str(line.split(":")[2].strip())
                    
                    self.variablesCount = int(line.split(":")[1].strip())
                
                    break
            else:
                raise Exception("No entry for %s in AutomationDB.cfg file, Plase Double check"%AutomationTool)
            #self.connect()
        except:
            raise

    def setLogger(self, loggerObject):
        self.mdbLog = loggerObject

    def cLog(self, *args):
        if self.mdbLog == False:
            self.trace.Debug(*args)
        else:
            self.mdbLog.Log(*args)
    
    def cLogException(self):
        if self.mdbLog == False:
            logMsg = "Exception Type: " + str(sys.exc_info()[0]) + "\n"
            logMsg += "Exception Details: " + str(sys.exc_info()[1]) + "\n"
            logMsg += "Exception Traceback: " + str(traceback.extract_tb(sys.exc_info()[2])) + "\n"
            self.trace.Debug(logMsg)
        else:
            self.mdbLog.LogException()
        
    def connect(self):
        self.connection = None
        self.cLog("Connecting to the Database:%s whose host is %s and port is %d"%(self.dataBaseName,self.host,self.port))
        self.cLog("Database Username:%s and Password:%s"%(self.user,self.password))
        try:
            self.connection = mdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.dataBaseName)
        except mdb.Error, e:
            self.cLog("Error %d: %s" % (e.args[0],e.args[1]))
            self.cLogException()
            raise
    def updateDB(self,variablesDict):
        try:
            #print "variableDict sent %s"%variablesDict
            #self.cursor = self.connection.cursor()
            if len(variablesDict.keys()) == self.variablesCount:
                updateQuery = self.dbQuery
                for var in variablesDict:
                    try:
                        updateQuery = updateQuery.replace('<%s_value>'%var,'%s'%variablesDict[var])
                    except e:
                        self.cLog("Error %d: %s" % (e.args[0],e.args[1]))
                        self.cLogException()

                self.cLog("updating Query: \n %s"%updateQuery)
                self.connect()
                self.cursor = self.connection.cursor()
                time.sleep(2)
                self.cursor.execute(updateQuery)
                time.sleep(2)
                self.connection.commit()
                time.sleep(2)
                self.close()
            else:
                self.cLog("Variable Count do not match please check again")

            
        except mdb.Error, e:
            self.cLog("Error %d: %s" % (e.args[0],e.args[1]))
            self.cLogException()
            raise
        
    def close(self):
        self.cLog("Closing the Database connection")
        try:
            if self.connection:
                self.connection.close()
        except mdb.Error, e:
            self.cLog("Error %d: %s" % (e.args[0],e.args[1]))
            self.cLogException()
            raise
    
    def __del__(self):
        if self.mdbLog:
            self.mdbLog.__del__()
        
if __name__ == "__main__":
    pass