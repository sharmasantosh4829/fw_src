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
import Trace
from Logger import *
import MySQLdb as mdb

class MySQLDataBase():
    
    def __init__(self,dataBaseHost, dataBasePort, dataBaseName, dataBaseUser, dataBasePassword):
        """
        Initialization function for the mdb
        """
        self.mdbLog = None
        self.host = dataBaseHost
        self.port = dataBasePort
        self.dataBaseName = dataBaseName
        self.user = dataBaseUser
        self.password = dataBasePassword
    
    def setLogger(self,loggerObject):
        self.mdbLog = loggerObject

    def connect(self):
        self.connection = None
        if self.mdbLog!=None:
            self.mdbLog.Info("Connecting to the Database:%s whose host is %s and port is %d"%(self.dataBaseName,self.host,self.port))
            self.mdbLog.Info("Database Username:%s and Password:%s"%(self.user,self.password))
        try:
            self.connection = mdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.dataBaseName)
        except mdb.Error, e:
            if self.mdbLog!=None:
                self.mdbLog.Error("Error %d: %s" % (e.args[0],e.args[1]))
                self.mdbLog.LogException()
            raise
    
    def executeSelectQuery(self,query,dictionaryCursor=False):
        self.cursor = None
        if self.mdbLog!=None:
            self.mdbLog.Info('Executing the query:%s'%query)
        try:
            if dictionaryCursor == False:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
            elif dictionaryCursor == True:
                self.cursor = self.connection.cursor(mdb.cursors.DictCursor)
                self.cursor.execute(query)
        except mdb.Error, e:
            if self.mdbLog!=None:
                self.mdbLog.Error("Error %d: %s" % (e.args[0],e.args[1]))
                self.mdbLog.LogException()
            raise
    
    def fetchAllRows(self):
        if self.mdbLog!=None:
            self.mdbLog.Info("Fetching all the rows in the table")
        try:
            rows = self.cursor.fetchall()
            if self.mdbLog!=None:
                self.mdbLog.Info("Rows fetched:%s"%(rows,))
            return rows
        except mdb.Error, e:
            if self.mdbLog!=None:
                self.mdbLog.Error("Error %d: %s" % (e.args[0],e.args[1]))
                self.mdbLog.LogException()
            raise
        
    def close(self):
        if self.mdbLog!=None:
            self.mdbLog.Info("Closing the Database connection")
        try:
            if self.connection:
                self.connection.close()
        except mdb.Error, e:
            if self.mdbLog!=None:
                self.mdbLog.Error("Error %d: %s" % (e.args[0],e.args[1]))
                self.mdbLog.LogException()
            raise
    
    def __del__(self):
        if self.mdbLog!=None:
            self.mdbLog.__del__()
        
if __name__ == "__main__":
    pass
