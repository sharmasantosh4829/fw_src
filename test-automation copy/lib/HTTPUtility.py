import os, sys
import time
from time import strftime

import urllib2,base64
from urllib2 import HTTPError
from urlparse import urlparse
from os.path import splitext, basename

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("HTTPUtility.py")), os.pardir)), "lib"))

from Logger import *

class HTTPUtility():
    
    def __init__(self):
        self.passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        self.tempDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("HTTPUtility.py")), os.pardir)), "temp")
        self.Logger = False
        
    def setLogger(self,loggerObject):
        self.Logger = loggerObject

        
    #Downloads from the "httpLink" optionally stores the information in the httpLink into localFileName
    #It also returns localFileName.
    #If localFileName is not provided, then the httpLink is stored in a file in "temp" directory and the name of the file is returned
    def download(self, httpLink, userName, password, localFileName = ""):
    
        if localFileName == "":
            localFileName = os.path.join(self.tempDir, strftime("tempFile_%Y-%m-%d_%H-%M-%S.tmp"))
            
        try:
            fp = open(localFileName,"wb")
        except:
            if self.Logger:
                self.Logger.LogException()
            raise
            
        try:
            self.passwordManager.add_password(None, httpLink, userName, password)
            self.handler = urllib2.HTTPBasicAuthHandler(self.passwordManager)
            self.opener = urllib2.build_opener(self.handler)
            response = self.opener.open(httpLink)
            fp.write(response.read())
            response.close()
            fp.close()
            if self.Logger:
                self.Logger.Log("Successfully downloaded from the link", httpLink, "to file", localFileName)
        except HTTPError, e:
            fp.close()
            if self.Logger:
                self.Logger.Log('Error, code: %s' % e.code)
                self.Logger.Log('Error: %s' % e.read())
            raise

        return localFileName
    
    
    #Downloads firmware file from Jenkins    
    def downloadFWFile(self, httpsLink, userName, password, localFileName):
        fp = open(localFileName,"wb") 
        try:         
            auth_encoded = base64.encodestring('%s:%s' % (userName, password))[:-1]        
            req = urllib2.Request(httpsLink)
            req.add_header('Authorization', 'Basic %s' % auth_encoded)
            response = urllib2.urlopen(req)
            fp.write(response.read())
            response.close()
            fp.close()
        except HTTPError, e:
            if self.Logger:
                self.Logger.Log('Error, code: %s' % e.code)
                self.Logger.Log('Error: %s' % e.read())
            raise

        return localFileName
            


if __name__ == "__main__":
    h = HTTPUtility()
    link = "http://192.168.1.109:49155/icon.jpg"
    print h.download(link,None,None,os.path.basename(link))
