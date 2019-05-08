import os, sys
import time
from time import strftime

import urllib
import urllib2, cookielib
from urllib2 import HTTPError

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("JenkinsUtility.py")), os.pardir)), "lib"))

from Logger import *

class JenkinsUtility():
    
    def __init__(self):
        self.securityCheckUrl = 'https://li-epssvn-prod-01.cisco.com:9000/j_acegi_security_check'
        self.tempDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("JenkinsUtility.py")), os.pardir)), "temp")
        self.Logger = False
        
    def setLogger(self,loggerObject):
        self.Logger = loggerObject


    #Downloads from the "httpsLink" optionally stores the information in the httpsLink into localFileName
    #It also returns localFileName.
    #If localFileName is not provided, then the httpsLink is stored in a file in "temp" directory and the name of the file is returned
    def download(self, httpsLink, userName, password, localFileName = ""):
    
        if localFileName == "":
            localFileName = os.path.join(self.tempDir, strftime("tempFile_%Y-%m-%d_%H-%M-%S.tmp"))
            
        try:
            fp = open(localFileName,"wb")
        except:
            if self.Logger:
                self.Logger.LogException()
            raise
            
        try:
            cookies = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
            data = {'j_username': '%s'%userName, 'j_password': '%s'%password, 'remember_me': 'false', 'from': '/', 'Submit': 'log in'}
            data = urllib.urlencode(data)
            try:
                response = opener.open(self.securityCheckUrl, data)
                response.close()
            except HTTPError, e:
                if self.Logger:
                    self.Logger.Log('Error, code: %s' % e.code)
                    self.Logger.Log('Error: %s' % e.read())
                fp.close()
                raise
                    
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
            response = opener.open(httpsLink)
            fp.write(response.read())
            response.close()
            fp.close()
            if self.Logger:
                self.Logger.Log("Successfully downloaded from the link", httpsLink, "to file", localFileName)
        except HTTPError, e:
            if self.Logger:
                self.Logger.Log('Error, code: %s' % e.code)
                self.Logger.Log('Error: %s' % e.read())
            raise

        return localFileName

        
