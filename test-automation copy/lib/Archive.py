import time, os, sys, traceback
from time import strftime
import zipfile
import shutil

from Trace import *

class Archive():

    def __init__(self):
        self.trace = Trace("Archive.py")
        self.LogDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("Archive.py")), os.pardir)), "logs")
        if not os.path.exists(self.LogDir):
            os.mkdir(self.LogDir)
            self.trace.Debug("Archive: Created LogDir: ", self.LogDir)
        self.tempDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("Archive.py")), os.pardir)), "temp")
        if not os.path.exists(self.tempDir):
            os.mkdir(self.tempDir)
            self.trace.Debug("Archive: Created tempDir: ", self.tempDir)
        
    def ArchiveLogs(self, moduleName, LogDir = None, archiveFile = None):
        
        if archiveFile == None:
            archiveFile = moduleName + "-" + strftime("%Y-%m-%d_%H-%M-%S") + ".zip"
        self.trace.Debug("tempDir: ", self.tempDir)

        if LogDir == None:
            LogDir = self.LogDir
        self.trace.Debug("LogDir: ", LogDir)
        zipFP = zipfile.ZipFile(os.path.join(r"%s"%self.tempDir, archiveFile), "w", zipfile.ZIP_DEFLATED)
        self.trace.Debug("zipFP: ", zipFP)

        CurDir = os.getcwd()
        os.chdir(r"%s"%LogDir)
        self.trace.Debug("LogDir: ", LogDir)


        try:
            contents = os.walk(".")
            noFileZipped = True

            for root, folders, files in contents:
                self.trace.Debug("root: ", root)
                self.trace.Debug("folders: ", folders)
                self.trace.Debug("files: ", files)

                # Include all subfolders, including empty ones.
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    self.trace.Debug("Adding '%s' to archive: "%absolute_path)
                    zipFP.write(absolute_path)
                    noFileZipped = False


                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    self.trace.Debug("Adding '%s' to archive: "%absolute_path)
                    zipFP.write('%s'%absolute_path)
                    noFileZipped = False

            zipFP.close()

            #delete all the files and folders from the logs folder
            contents = os.walk(".")
            for root, folders, files in contents:
                for folder_name in folders:
                    shutil.rmtree(folder_name)            

                for file_name in files:
                    os.remove(file_name)

            if noFileZipped == True:
                self.trace.Warning("Deleting the empty archive file '%s'"%archiveFile)
                os.remove(os.path.join(r"%s"%self.tempDir, archiveFile))
                archiveFile = ""
            else:
                self.trace.Debug("Archive File Created", archiveFile)
                archiveFile = os.path.join(r"%s"%self.tempDir, archiveFile)

        except:
            pass
            # Issue while working on silenium firefox ( firefox cannot be closed as per requirements)
            self.trace.Critical(sys.exc_info()[0])
            self.trace.Critical(sys.exc_info()[1])
            self.trace.Critical(traceback.extract_tb(sys.exc_info()[2]))
            '''
            archiveFile = ""
            '''

        os.chdir(r"%s"%CurDir)

        return archiveFile
    
    def ArchiveFileList(self, moduleName, LogDir = None, archiveFile = None , fileList=[]):
        
        if archiveFile == None:
            archiveFile = moduleName + "-" + strftime("%Y-%m-%d_%H-%M-%S") + ".zip"
        self.trace.Debug("tempDir: ", self.tempDir)

        if LogDir == None:
            LogDir = self.LogDir
        self.trace.Debug("LogDir: ", LogDir)
        zipFP = zipfile.ZipFile(os.path.join(r"%s"%self.tempDir, archiveFile), "w", zipfile.ZIP_DEFLATED)
        self.trace.Debug("zipFP: ", zipFP)

        CurDir = os.getcwd()
        os.chdir(r"%s"%LogDir)
        self.trace.Debug("LogDir: ", LogDir)


        try:
            contents = os.walk(".")
            noFileZipped = True

            for root, folders, files in contents:
                self.trace.Debug("root: ", root)
                self.trace.Debug("folders: ", folders)
                self.trace.Debug("files: ", files)


                for file_name in files:
                    if file_name in fileList:
                        absolute_path = os.path.join(root, file_name)
                        self.trace.Debug("Adding '%s' to archive: "%absolute_path)
                        zipFP.write('%s'%absolute_path)
                        noFileZipped = False

            zipFP.close()

            #delete all the files and folders from the logs folder
            contents = os.walk(".")
            for root, folders, files in contents:
                for file_name in files:
                    if file_name in fileList:
                        os.remove(file_name)

            if noFileZipped == True:
                self.trace.Warning("Deleting the empty archive file '%s'"%archiveFile)
                os.remove(os.path.join(r"%s"%self.tempDir, archiveFile))
                archiveFile = ""
            else:
                self.trace.Debug("Archive File Created", archiveFile)
                archiveFile = os.path.join(r"%s"%self.tempDir, archiveFile)

        except:
            pass
            # Issue while working on silenium firefox ( firefox cannot be closed as per requirements)
            self.trace.Critical(sys.exc_info()[0])
            self.trace.Critical(sys.exc_info()[1])
            self.trace.Critical(traceback.extract_tb(sys.exc_info()[2]))
            '''
            archiveFile = ""
            '''

        os.chdir(r"%s"%CurDir)

        return archiveFile

    def ArchiveLogsWithoutDelete(self, moduleName, LogDir = None, archiveFile = None):
        
        if archiveFile == None:
            archiveFile = moduleName + "-" + strftime("%Y-%m-%d_%H-%M-%S") + ".zip"
        self.trace.Debug("tempDir: ", self.tempDir)

        if LogDir == None:
            LogDir = self.LogDir
        self.trace.Debug("LogDir: ", LogDir)
        zipFP = zipfile.ZipFile(os.path.join(r"%s"%self.tempDir, archiveFile), "w", zipfile.ZIP_DEFLATED)
        self.trace.Debug("zipFP: ", zipFP)

        CurDir = os.getcwd()
        os.chdir(r"%s"%LogDir)
        self.trace.Debug("LogDir: ", LogDir)


        try:
            contents = os.walk(".")
            noFileZipped = True

            for root, folders, files in contents:
                self.trace.Debug("root: ", root)
                self.trace.Debug("folders: ", folders)
                self.trace.Debug("files: ", files)

                # Include all subfolders, including empty ones.
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    self.trace.Debug("Adding '%s' to archive: "%absolute_path)
                    zipFP.write(absolute_path)
                    noFileZipped = False


                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    self.trace.Debug("Adding '%s' to archive: "%absolute_path)
                    zipFP.write('%s'%absolute_path)
                    noFileZipped = False

            zipFP.close()

            if noFileZipped == True:
                self.trace.Warning("Deleting the empty archive file '%s'"%archiveFile)
                os.remove(os.path.join(r"%s"%self.tempDir, archiveFile))
                archiveFile = ""
            else:
                self.trace.Debug("Archive File Created", archiveFile)
                archiveFile = os.path.join(r"%s"%self.tempDir, archiveFile)

        except:
            pass
            # Issue while working on silenium firefox ( firefox cannot be closed as per requirements)
            self.trace.Critical(sys.exc_info()[0])
            self.trace.Critical(sys.exc_info()[1])
            self.trace.Critical(traceback.extract_tb(sys.exc_info()[2]))
            '''
            archiveFile = ""
            '''

        os.chdir(r"%s"%CurDir)

        return archiveFile




    def ArchiveSpecificFiles(self, archiveName, filesList, LogDir = None):
        
        archiveFile = archiveName + "-" + strftime("%Y-%m-%d_%H-%M-%S") + ".zip"
        self.trace.Debug("tempDir: ", self.tempDir)
        
        if LogDir == None:
            LogDir = self.LogDir
        self.trace.Debug("LogDir: ", LogDir)
        zipFP = zipfile.ZipFile(os.path.join(r"%s"%self.tempDir, archiveFile), "w", zipfile.ZIP_DEFLATED)
        self.trace.Debug("zipFP: ", zipFP)

        CurDir = os.getcwd()
        os.chdir(r"%s"%LogDir)
        self.trace.Debug("LogDir: ", LogDir)
        


        try:
            contents = os.walk(".")
            noFileZipped = True

            for root, folders, files in contents:
                self.trace.Debug("root: ", root)
                self.trace.Debug("folders: ", folders)
                self.trace.Debug("files: ", files)
                '''
                # Include all subfolders, including empty ones.
                for folder_name in folders:
                    absolute_path = os.path.join(root, folder_name)
                    self.trace.Debug("Adding '%s' to archive: "%absolute_path)
                    zipFP.write(absolute_path)
                    noFileZipped = False
                '''

                for file_name in files:
                    if file_name in filesList:
                        absolute_path = os.path.join(root, file_name)
                        self.trace.Debug("Adding '%s' to archive: "%absolute_path)
                        zipFP.write('%s'%absolute_path)
                        noFileZipped = False

            
            zipFP.close()
            
            #delete specific files from the logs folder
            contents = os.walk(".")
            for root, folders, files in contents:
                '''
                for folder_name in folders:
                    shutil.rmtree(folder_name)            
                '''
                for file_name in files:
                    if file_name in filesList:
                        os.remove(file_name)
            

            if noFileZipped == True:
                self.trace.Warning("Deleting the empty archive file '%s'"%archiveFile)
                os.remove(os.path.join(r"%s"%self.tempDir, archiveFile))
                archiveFile = ""
            else:
                self.trace.Debug("Archive File Created", archiveFile)
                archiveFile = os.path.join(r"%s"%self.tempDir, archiveFile)
                print archiveFile

        except:
            pass
            '''
            # Issue while working on silenium firefox ( firefox cannot be closed as per requirements)
            self.trace.Critical(sys.exc_info()[0])
            self.trace.Critical(sys.exc_info()[1])
            self.trace.Critical(traceback.extract_tb(sys.exc_info()[2]))
            archiveFile = ""
            '''

        os.chdir(r"%s"%CurDir)

        return archiveFile

