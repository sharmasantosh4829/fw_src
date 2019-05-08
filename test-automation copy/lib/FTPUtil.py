import ftplib
import os, sys, traceback
import Trace


class FTPUtil():
    
    #def __init__(self, reportServer = "172.25.17.53", userName = "ftpuser", password = "belkin123", homedir = "/home/ftpuser/log/Archives/", uploadLink = "ftp://ftpuser:belkin123@172.25.17.53/log/Archives/"):
    def __init__(self, reportServer = "54.183.199.137", userName = "qe", password = "quality1st", homedir = "/test-automation/LogArchives/", uploadLink = "ftp://qe:quality1st@54.183.199.137/test-automation/LogArchives/"):    
        self.REPORT_SERVER = reportServer
        self.RS_USERNAME = userName
        self.RS_PASSWORD = password
        self.RS_HOMEDIR = homedir
        self.UPLOAD_LINK = uploadLink
        self.trace = Trace.Trace("FTPUtil.py")
        
        self.ftpHandle = None
        try:    
            self.ftpHandle = ftplib.FTP(self.REPORT_SERVER)
            #self.ftpHandle.set_pasv(False)
            self.ftpHandle.close()
        except:
            self.trace.Critical(sys.exc_info()[0])
            self.trace.Critical(sys.exc_info()[1])
            self.trace.Critical(traceback.extract_tb(sys.exc_info()[2]))
        
    def uploadFile(self, filePath, projectDir):
        self.ftpHandle.cwd(self.RS_HOMEDIR)
        fileList = self.ftpHandle.nlst()
        if projectDir not in fileList:
            self.trace.Info("Dir does not exist .. so creating directory", projectDir)
            self.ftpHandle.mkd(projectDir)
        self.ftpHandle.cwd(projectDir)
        f = open(filePath, "rb")
        self.ftpHandle.storbinary("STOR %s"%(os.path.basename(filePath)), f)
        f.close()
        
        
    def uploadArchiveToServer(self, filePath, projectDir):
        if not os.path.exists(r'%s'%filePath):
            raise Exception("Archive File does not exist", filePath)
        self.trace.Debug(self.REPORT_SERVER)
        self.trace.Debug(self.RS_USERNAME)
        self.trace.Debug(self.RS_PASSWORD)
        self.ftpHandle = ftplib.FTP(self.REPORT_SERVER)
        self.ftpHandle.login(self.RS_USERNAME, self.RS_PASSWORD)
        #self.ftpHandle.set_pasv(False)
        
        self.uploadFile(filePath, projectDir)
        self.ftpHandle.quit()
        self.ftpHandle = None
        self.trace.Debug("Archive of Test Logs uploaded to Report Server ..returing the uploaded file link")
        uploadLink = self.UPLOAD_LINK + projectDir + "/" + os.path.basename(filePath)
        self.trace.Debug("returned the link", uploadLink)
        return uploadLink
        
        
if __name__ == "__main__":
    f = FTPUtil()
    tempDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("FTPUtil.py")), os.pardir)), "temp")
    prjName = "WeMoUPnPTestDevice"
    filesToUpload = []
    for flname in filesToUpload:
        f.uploadArchiveToServer(os.path.join(tempDir,flname), prjName)