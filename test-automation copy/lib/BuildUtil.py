'''
/*
* Copyright (c) 2010 Cisco Systems, Inc. All rights reserved.
*
* Cisco Systems, Inc. retains all right, title and interest (including all
* intellectual property rights) in and to this computer program, which is
* protected by applicable intellectual property laws.  Unless you have obtained
* a separate written license from Cisco Systems, Inc., you are not authorized
* to utilize all or a part of this computer program for any purpose (including
* reproduction, distribution, modification, and compilation into object code),
* and you must immediately destroy or return to Cisco Systems, Inc. all copies
* of this computer program.  If you are licensed by Cisco Systems, Inc., your
* rights to utilize this computer program are limited by the terms of that
* license.  To obtain a license, please contact Cisco Systems, Inc.
*
* This computer program contains trade secrets owned by Cisco Systems, Inc.
* and, unless unauthorized by Cisco Systems, Inc. in writing, you agree to
* maintain the confidentiality of this computer program and related information
* and to not disclose this computer program and related information to any
* other person or entity.
*
* THIS COMPUTER PROGRAM IS PROVIDED AS IS WITHOUT ANY WARRANTIES, AND CISCO
* SYSTEMS, INC. EXPRESSLY DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED,
* INCLUDING THE WARRANTIES OF MERCHANTIBILITY, FITNESS FOR A PARTICULAR
* PURPOSE, TITLE, AND NONINFRINGEMENT.
*/
'''


import urllib
import urllib2, cookielib
from urllib2 import HTTPError
import re
import os
from time import sleep
from time import strftime
import subprocess
import Trace


#UpgradeLatestFirmware('EA3500')
class BuildUtil():
    
    def __init__(self):
        #check if the entry exists in buildlocations for the routername
        self.trace = Trace.Trace("BuildUtil.py")
        self.tempdirName = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("BuildUtil.py")), os.pardir)), "temp")
        if not os.path.exists(self.tempdirName):
                os.mkdir(self.tempdirName)
        self.fwBuildsPath = os.path.join(self.tempdirName,'FWBuilds')
        if not os.path.exists(self.fwBuildsPath):
                os.mkdir(self.fwBuildsPath)
        else:
            
            self.trace.Info("BuildsDir Already Exists")
            pass
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))  
        self.configPath = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("BuildUtil.py")), os.pardir)), "config")
        self.buildLocationPath = os.path.join(self.configPath,'build_locations.txt')
        self.urlinput = {'j_username': 'rainier_test', 'j_password': '84902849302hupeue', 'remember_me': 'false', 'from': '/', 'Submit': 'log in'}
        self.urldata = urllib.urlencode(self.urlinput)
        self.hudsonSecurityURL = 'https://li-epssvn-prod-01.cisco.com:9000/j_acegi_security_check'
        self.updateShellScript = "latest_update.sh"
        self.a = self.b = 0
        self.trace.Info(self.configPath)
        self.trace.Info(self.buildLocationPath)
        
        try:
            if not os.path.exists(self.buildLocationPath):
                if not os.path.exists('latest_update.sh'):
                    raise Exception("buildLocationpath or latestupdate file does not exist")
        except Exception as exp:
            self.trace.Critical("Unexpected error: %s" %exp)
            
    def VerifyRouterEntries(self, routerName):
        try:
            f = open(self.buildLocationPath, 'r')
            for line in f.readlines():
                if line.find('#') == 0:
                    continue
                if line.find(routerName) != -1:
                    self.trace.Info('entry for %s found in buildLocation.txt'%routerName)
                    self.b += 1
                    
                else:
                    pass      
            f.close()
            #check if the routername is takencare of in the latest_update.sh file
            f = open('latest_update.sh', 'r')
            for line in f.readlines():
                if routerName in line:
                    self.trace.Info('routerName present in latest_update.sh')
                    self.a += 1
                    break
            f.close()
            if self.a == 0 or self.b == 0:
                raise Exception("routerName not present in latest_update.sh or buildLocation.txt")
            else:
                return True
            
        except Exception as exp:
            self.trace.Critical("Unexpected error: %s" %exp)
            
    
    def customURLjoin(self, *args):
        return "/".join(map(lambda x: str(x).rstrip('/'), args))
        
    

    def GetAndCheckBuildLocation(self,routerName, serverPath = None, fwBuildNumber = None):
        buildInfo = {}
        routerFileName = fileExtension = errorCode = None
        #cookies = cookielib.CookieJar()
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        #urldata = {'j_username': 'rainier_test', 'j_password': '84902849302hupeue', 'remember_me': 'false', 'from': '/', 'Submit': 'log in'}
        #urldata = urllib.urlencode(urldata)
        try:
            #url = 'https://li-epssvn-prod-01.cisco.com:9000/j_acegi_security_check'
            #response = opener.open(url, urldata)
            response = self.opener.open(self.hudsonSecurityURL, self.urldata)
            response.close()
        except HTTPError, e:
            print 'Error, code: %s' % e.code
            print 'Error: %s' % e.read()
                
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        g = open(self.buildLocationPath, 'r')
        for line in g.readlines():
            #print line
            if line.find('#') == 0:
                print line
                continue
            if line.find(routerName) != -1:
                line = line[:-1]
                data = line.split(';')
                buildInfo["routerName"] = routerName
                if serverPath != None and fwBuildNumber == None:
                    #print " inside serverPath"
                    self.trace.Info("server path \n %s"%serverPath)
                    updatedServerPath = self.customURLjoin(serverPath,'lastStableBuild/artifact/nfsroot/')
                    #print updatedServerPath
                    buildInfo["buildLocation"] = updatedServerPath
                    #print buildInfo["buildLocation"]
                elif serverPath != None and fwBuildNumber != None:
                    try:
                        #print "inside serverpath and fwbuildnumber"
                        response = self.opener.open(self.hudsonSecurityURL, self.urldata)
                        response.close()
                        #print serverPath
                        #print urldata
                        response = self.opener.open(serverPath,urldata)
                        html_content = response.read()
                        buildmatches = re.search('\/([0-9]{2,3})\/(.*)(%s)'%fwBuildNumber, html_content)
                        routernamematch = re.search(routerName, html_content)
                        if routernamematch:
                            self.trace.Info("inside router name match")
                            if buildmatches: 
                               self.trace.Info('found the build number')
                               buildID = buildmatches.group(1).strip()
                               updatedServerPath = str(self.customURLjoin(serverPath,'lastStableBuild/artifact/nfsroot/'))
                               #print updatedServerPath
                               #updatedServerPath = str(os.path.join(serverPath,'lastStableBuild/artifact/nfsroot/'))
                               updatedServerPath = updatedServerPath.replace("lastStableBuild", buildID)
                               #print updatedServerPath
                               buildInfo["buildLocation"] = updatedServerPath
                               
                            else:
                               return "Did not find the FW build on the provided server Path"
                        elif serverPath == None and fwBuildNumber != None:
                            return "Please specify serverPath when specifying Fw Build number"
                        else:
                            return "Given Serverpath does not relate to the %s"%routerName
                            
                        
                    except HTTPError, e:
                        self.trace.Critical('Error, code: %s' % e.code)
                        self.trace.Critical('Error: %s' % e.read())
                else:
                    buildInfo["buildLocation"] = data[1]
                buildInfo["fileExtension"] = data[2]
                #routerBuildLocation = data[1]
                #fileExtension = data[2]
            
        g.close()
        try:
            #print "inside checking"
            if buildInfo["buildLocation"] != None:
                url = buildInfo["buildLocation"]
                response = self.opener.open(url)
                response.close()
        except HTTPError, e:
            errorCode = e.code
            self.trace.Critical('Error, code: %s' % e.code)
            self.trace.Critical('Error: %s' % e.read())
        if errorCode == None:
            if buildInfo["buildLocation"] != None:
                buildInfo["buildDotTxtPath"] = buildInfo["buildLocation"].split('/nfsroot')[0]+'/build.txt'
                try:
                    url = buildInfo['buildDotTxtPath']
                    response = self.opener.open(url)
                    buildTxtPage = response.read()
                    buildIDMatch = re.search('build_id:(.*)([0-9]{2,3})',buildTxtPage)
                    versionMatch = re.search('version:(.*)',buildTxtPage)
                    if buildIDMatch:
                        buildInfo["buildID"] = buildIDMatch.group(2).strip()
                        #print buildInfo["buildID"]
                    else:
                        self.trace.Error("Could not find build ID in build.txt")
                    
                    if versionMatch:
                        buildInfo["fwVersion"] = versionMatch.group(1).strip()
                        #print buildInfo["fwVersion"]
                    else:
                        self.trace.Error("Could not find version in build.txt")
                    response.close()
                except HTTPError, e:
                    self.trace.Critical('Error, code: %s' % e.code)
                    self.trace.Critical('Error: %s' % e.read())
                buildInfo["FWFileName"] =  "FW_%s_%s_release.%s" %(buildInfo["routerName"],buildInfo["fwVersion"],buildInfo["fileExtension"])       
                buildInfo["hudsonImageFilePath"] = buildInfo["buildLocation"]+buildInfo["FWFileName"]
                
                
                #print 'routerName inside: %s\n' %routerName
                if routerName in ("EA6500", "EA6300", "EA6400", "EA6700"):
                    #print "entered routername pinnacle"
                    #imageFileName = buildInfo["FWFileName"]
                    f = open(self.updateShellScript,'r')
                    filedata = f.read()
                    f.close
                    #print filedata
                    regex = re.compile(r'FWFileName.trx',re.MULTILINE)
                    newfiledata = regex.sub(buildInfo["FWFileName"],filedata)
                    #print 'after modification'
                    #print newfiledata
                    modifiedShellScript = buildInfo["routerName"]+"_"+buildInfo["fwVersion"]+'_script'+'.sh'
                    f = open(modifiedShellScript,'w')
                    f.write(newfiledata)
                    f.close
                    buildInfo["ShellScriptName"] = modifiedShellScript
                    #print buildInfo["ShellScriptName"]
                elif routerName == "EA2700":
                    buildInfo["ShellScriptName"] = "linux.trx"
                elif routerName == "EA4500":
                    buildInfo["ShellScriptName"] = "viper.128mb.img"
                elif routerName == "EA3500":
                    buildInfo["ShellScriptName"] = "audi.img"
                #print "IN GetAndCheckFW:\n%s"%buildInfo
                return buildInfo
        else:
            return "Not able to access the buildLocation: %s"%errorCode

    def GetFirmwareBuild(self,buildInfo = None):
        if not os.path.exists(os.path.join(self.fwBuildsPath,buildInfo["routerName"])):
                os.mkdir(os.path.join(self.fwBuildsPath,buildInfo["routerName"]))
        else: 
            self.trace.Info("Router %s Dir Already Exists" %buildInfo["routerName"])
            pass
        FileName = buildInfo["FWFileName"]
        self.trace.Info("FileName: %s"%FileName)
        fwImageFilePath = os.path.join(os.path.join(self.fwBuildsPath,buildInfo["routerName"]),FileName)
        self.trace.Info("fwImageFilePath: %s"%fwImageFilePath)
        try:
            response = self.opener.open(self.hudsonSecurityURL, self.urldata)
            response.close()
            sleep(10)
            if not os.path.exists(fwImageFilePath):
                self.trace.Info("hudsonImageFilePath: %s"%buildInfo["hudsonImageFilePath"])
                response = self.opener.open(buildInfo["hudsonImageFilePath"])
                fileSizeBeforeDownload = len(response.read())
                response.close()
                sleep(10)                      
                f = open(fwImageFilePath, 'wb')
                response = self.opener.open(buildInfo["hudsonImageFilePath"])
                f.write(response.read())
                response.close()
                f.close()
                f = open(fwImageFilePath, 'rb')
                fileSizeAfterDownload = len(f.read())
                f.close()
                if fileSizeBeforeDownload == fileSizeAfterDownload:
                    buildInfo["fwImageFilePath"] = fwImageFilePath
                #print buildInfo
                return buildInfo
            else:
                buildInfo["fwImageFilePath"] = fwImageFilePath
                self.trace.Info("FW Image Already exists")
                self.trace.Info("IN GetFwBuild: \n%s"%buildInfo)
                return buildInfo
        except HTTPError, e:
            self.trace.Critical('Error, code: %s' % e.code)
            self.trace.Critical('Error: %s' % e.read())
    
   
    
    def FirmwareUpdate(self,routerName,serverPath = None,fwBuildNumber = None):
        if self.VerifyRouterEntries(routerName):
            buildInfo = self.GetAndCheckBuildLocation(routerName, serverPath, fwBuildNumber)
            #print buildInfo
            buildInfo = self.GetFirmwareBuild(buildInfo)
            #print buildInfo
            #print 'filePath: %s\n' %(buildInfo["fwImageFilePath"])
            ScriptName = buildInfo["ShellScriptName"]
            
            process = subprocess.Popen("plink -auto_store_key_in_cache -batch -ssh -l root -pw admin myrouter.local su root -c 'cat /etc/version'", shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            if output != None:
                #f.write('creating downloads dir if not exists\,'+output+'\n')
                print 'current FW version on the router %s'%output
            if stderr:
                #f.write('Error:'+stderr+'\n')
                return 'Error'
            self.trace.Info(output)
            sleep(30)
            self.trace.Info("FW file Upload: STARTED\n")
            #print buildInfo["FWFileName"]
            process = subprocess.Popen("pscp.exe -scp -pw admin %s root@myrouter.local:/var/config/%s"%(buildInfo["fwImageFilePath"], buildInfo["FWFileName"]), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            if output != None:
                #f.write('file downloaded to /var/config/\n'+output+'\n')
                self.trace.Info('file downloaded to /var/config/')
                self.trace.Info("FW file Upload: COMPLETE\n")
            if stderr:
                #f.write('Error while file downloading:'+stderr+'\n')
                return 'Error'
            print output
            sleep(30)
            self.trace.Info("Script Upload: STARTED")
            process = subprocess.Popen("pscp.exe -scp -pw admin %s root@myrouter.local:/var/config/"%buildInfo["ShellScriptName"], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            print output
            if output != None:
                #f.write('Script downloaded to /var/config/downloads\n'+output+'\n')
                self.trace.Info('Script downloaded to /var/config/')
                self.trace.Info("Script Upload: COMPLETE")
            if stderr:
                #f.write('Error while script download:\n'+stderr+'\n')
                return 'Error'
            sleep(30)
            self.trace.Info("Script mode change: STARTED")
            process = subprocess.Popen("plink -ssh -l root -pw admin myrouter.local dos2unix /var/config/%s"%buildInfo["ShellScriptName"], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            print output
            if output != None:
                #f.write('Script mode change to dos2unix\n'+output+'\n')
                self.trace.Info( 'Script mode change to dos2unix')
                
            if stderr:
                #f.write('Error while changing mode:\n'+stderr+'\n')
                return stderr
            sleep(30)
            
            process = subprocess.Popen("plink -ssh -l root -pw admin myrouter.local chmod 777 /var/config/%s"%buildInfo["ShellScriptName"], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            if output != None:
                #f.write('Script mode change to executable\n'+output+'\n')
                self.trace.Info( 'Script mode change to executable')
                self.trace.Info( "Script mode change: COMPLETE")
            if stderr:
                #f.write('Error while changing to executable:\n'+stderr+'\n')
                return stderr
            self.trace.Info( output)
            sleep(30)
            self.trace.Info( "Executing script: STARTED")
            process = subprocess.Popen("plink -ssh -l root -pw admin myrouter.local /bin/sh /var/config/%s"%buildInfo["ShellScriptName"], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            if output != None:
                #f.write('Executing the script\n'+output+'\n')
                self.trace.Info( 'Executing the script')
                self.trace.Info( "Executing script: COMPLETE")
            if stderr:
                #f.write('Error while executing script:\n'+stderr+'\n')
                return stderr
            self.trace.Info( output)
            self.trace.Info( "sleeping for 200 sec")
            sleep(200)
            
            self.trace.Info( "Executing script after reboot: STARTED")
            process = subprocess.Popen("plink -ssh -l root -pw admin myrouter.local /bin/sh /var/config/%s"%buildInfo["ShellScriptName"], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            if output != None:
                #f.write('Executing the script again after reboot\n'+output+'\n')
                
                self.trace.Info( "Executing script: COMPLETE")
            if stderr:
                #f.write('Error:'+stderr+'\n')
                return stderr
            self.trace.Info( output)
            self.trace.Info( "sleeping for 200 sec")
            sleep(200)
            
            self.trace.Info( "Removing Script Files: STARTED")
            process = subprocess.Popen("plink -ssh -l root -pw admin myrouter.local rm /var/config/%s"%buildInfo["ShellScriptName"], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            if output != None:
                #f.write('Removing script on the router\n'+output+'\n')
                self.trace.Info( 'Removing script on the router')
              
            if stderr:
                #f.write('Error:'+stderr+'\n')
                return stderr
            self.trace.Info( output)
            sleep(30)
            
            process = subprocess.Popen("plink -ssh -l root -pw admin myrouter.local rm /var/config/%s"%buildInfo["FWFileName"], shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output,stderr = process.communicate()
            if output != None:
                #f.write('Removing firmware on the router\n'+output+'\n')
                self.trace.Info( 'Removing firmware on the router')
              
            if stderr:
                #f.write('Error:'+stderr+'\n')
                return stderr
            self.trace.Info( output)
            os.remove(buildInfo["ShellScriptName"])
            self.trace.Info( 'Removing Script files: COMPLETE')
            sleep(30)
            
            process = subprocess.Popen("plink -ssh -l root -pw admin myrouter.local cat /etc/version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, stderr = process.communicate()
            #latestFWVersion = GetLatestStableBuildVersion(routerName)
            if output.strip() == buildInfo["fwVersion"]:
                self.trace.Info( 'Router is upgraded to the latest version %s\n'%output)
                #f.write('Router is upgraded to the latest version %s\n'%output)
                return True
            else:
                self.trace.Info( 'Error: Falied router upgrade\n')
                #f.write('Error: Falied router upgrade\n')
                return False
         

