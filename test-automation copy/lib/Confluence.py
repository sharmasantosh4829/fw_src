import os
import xmlrpclib
from xmlrpclib import Server
import re, sys
import traceback
from Trace import *


class Confluence():
    def __init__(self, configFile):
        self.configFile = configFile
        self.server = Server('http://wiki.nikleb.com:8090/rpc/xmlrpc')
        self.updateDict = {}
        self.PAGE_ID = ""
        self.logger = False
        self.configPath = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("Confluence.py")), os.pardir)), "config")
        self.logDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("Confluence.py")), os.pardir)), "logs")
        self.trace = Trace("Confluence.py")
        
    def setLogger(self, loggerObject):
        self.logger = loggerObject
        
    def cLog(self, *args):
        if self.logger == False:
            self.trace.Debug(*args)
            print args
        else:
            self.logger.Log(*args)
    
    def cLogException(self):
        if self.logger == False:
            logMsg = "Exception Type: " + str(sys.exc_info()[0]) + "\n"
            logMsg += "Exception Details: " + str(sys.exc_info()[1]) + "\n"
            logMsg += "Exception Traceback: " + str(traceback.extract_tb(sys.exc_info()[2])) + "\n"
            self.trace.Debug(logMsg)
            print logMsg
        else:
            self.logger.LogException()

    def ReadConfigFile(self):
        #read Confluence page details from the file self.configFile in the config folder
        if not os.path.exists(os.path.join(self.configPath, self.configFile)):
            self.cLog("No config file: ", self.configFile)
        else:
            fp = open(os.path.join(self.configPath, self.configFile), "r")
            lines = fp.readlines()
            fp.close()
            
            if len(lines) == 0:
                self.cLog("Empty config file: ", self.configFile)
            else:
                for line in lines:
                    if line.find("#") == 0:
                        continue
                    if line.strip() == "":
                        continue
                    else:
                        exec(line)
    
        self.cLog("Page Title:", PAGE_TITLE)
        self.PAGE_TITLE = PAGE_TITLE
        self.cLog("Page Space:", PAGE_SPACE_NAME)
        self.PAGE_SPACE_NAME = PAGE_SPACE_NAME
        self.cLog("Table Name:", TABLE_NAME)
        self.TABLE_NAME = TABLE_NAME
        self.cLog("Column Names:", ALL_COLUMN_NAMES)
        self.ALL_COLUMN_NAMES = ALL_COLUMN_NAMES.split(",")
        self.cLog("HTTP Link Column Names:", HTTP_LINK_COLUMN_NAMES)
        self.HTTP_LINK_COLUMN_NAMES = HTTP_LINK_COLUMN_NAMES.split(",")
        self.cLog("Attachment Column Names:", ATTACHMENT_COLUMN_NAMES)
        if ATTACHMENT_COLUMN_NAMES != "":
            tempArray = ATTACHMENT_COLUMN_NAMES.split(",")
        else:
            tempArray = []
        self.ATTACHMENT_COLUMN_NAMES = []
        self.CONTENT_TYPE = {}
        for column in tempArray:
            if column.find(";") > -1:
                attachmentColumnName = column.split(";")[0].strip()
                attachmentType = column.split(";")[1].strip()
                self.ATTACHMENT_COLUMN_NAMES.append(attachmentColumnName)
                self.CONTENT_TYPE[attachmentColumnName] = attachmentType
            else:
                self.cLog("Invalid Config File Format", self.configFile)
                return False
                
        
    def Login(self):
        self.token = self.server.confluence2.login('qe_automation', '8092#ueoau$')
        return self.token
        
       
    def CreatePage(self):
        addStr = '<h1>' + self.TABLE_NAME + '</h1><table><tbody><tr>'
        for column in self.ALL_COLUMN_NAMES:
            addStr += '<th colspan="1">' + column + '</th>'
        addStr += '</tr></tbody></table>'
        page = {}
        page['title'] = self.PAGE_TITLE
        page['space'] = self.PAGE_SPACE_NAME
        page['content'] = addStr
        self.server.confluence2.storePage(self.token, page)
        time.sleep(5)
        return self.server.confluence2.getPage(self.token, self.PAGE_SPACE_NAME, self.PAGE_TITLE)
        
        
    def GetPage(self, token = None, pageSpace = None, pageTitle = None):
        if pageTitle == None:
            pageTitle = self.PAGE_TITLE
        if pageSpace == None:
            pageSpace = self.PAGE_SPACE_NAME
        if token == None:
            token = self.token
        return self.server.confluence2.getPage(token, pageSpace, pageTitle)

        
    def PrepareUpdateString(self):
        updateStr = '<tr>'
        for column in self.ALL_COLUMN_NAMES:
            if column in self.HTTP_LINK_COLUMN_NAMES:
                links = str(self.updateDict[column]).split(" ")
                updateStr += '<td>'
                for link in links:
                    updateStr += '<a href="%s" rel="nofollow">%s</a><br><br>'%(link, link)
                updateStr += '</td>'
            elif column in self.ATTACHMENT_COLUMN_NAMES:
                updateStr += '<td><ac:link><ri:attachment ri:filename="%s" /></ac:link></td>'%str(self.updateDict[column])
            else:
                updateStr += '<td>%s</td>'%str(self.updateDict[column])
        updateStr += '</tr>'
        return updateStr
    
    
    def GetUpdatedContent(self, content, updateString):
        #search for the table name in the content
        searchStr = '<tr>'
        for column in self.ALL_COLUMN_NAMES:
            escapedColumnName = re.escape(column)
            searchStr += '<th.*>.*%s.*</th>'%escapedColumnName
        searchStr += '</tr>'
        escapedTableName = re.escape(self.TABLE_NAME)
        searchPattern = '(%s.*<table>.*<tbody>%s)(.*)'%(escapedTableName, searchStr)
        self.trace.Debug(searchPattern)
        matchObj = re.compile(searchPattern)
        if matchObj == None:
            self.cLog("matchObj is None")
            return content
        searchResults = matchObj.findall(content)
        self.trace.Debug(searchResults)
        if len(searchResults) > 0:
            self.trace.Debug("Found the table & its header")
            searchResults = searchResults[0]
            if len(searchResults) > 0:
                self.trace.Debug("Found the table header & its header-2")
                searchString = searchResults[0]
                searchIndex = content.find(searchString)
                #Insert the updateString after the searchIndex
                content = content[:searchIndex + len(searchString)] + updateString + content[searchIndex + len(searchString):]
                content = content.replace("<br>", "<br/>")
                self.trace.Debug("Updated Content", content)
                return content
            else:
                self.cLog("Could not find the table-2")
                self.trace.Debug("Content", content)
                return content
        else:
            self.cLog("Could not find the table")
            self.trace.Debug("Content", content)
            return content
        
        
    def AttachFileToConfluencePage(self, pageId, fileName, contentType):
        try:
            self.trace.Debug("fileName:", fileName)
            with open(fileName, "rb") as f:
                data = f.read()
            
            attachment = {};
            attachment['fileName'] = os.path.basename(fileName);
            attachment['contentType'] = contentType;
             
            self.server.confluence2.addAttachment(self.token, pageId, attachment, xmlrpclib.Binary(data));
            return True
        except:
            self.cLogException()
            self.cLog("Could not attach file:", fileName)
            return False


        
    def UpdateConfluencePage(self, *args):
        try:
            #Read the config file
            self.ReadConfigFile()
        except:
            self.cLogException()
            self.cLog("Could not read config file:", self.configFile)
            return False

        #Login
        try:
            self.token = self.Login()
        except:
            self.cLogException()
            self.cLog("Could not login")
            return False

        #Get the Page
        try: 
            page = self.GetPage()
            if page == None:
                page = self.CreatePage()
            self.PAGE_ID = page['id']
        except Exception, e:
            if re.search('it does not exist', str(e)):
                self.cLog("it does not exist .. so creating the page")
                page = self.CreatePage()
                self.PAGE_ID = page['id']
        else:
            pass
           
            
        #Prepare the dictionary with the values that need to be updated to the Page
        if len(args) != len(self.ALL_COLUMN_NAMES):
            self.cLog("argument number mismatch .. exiting")
            return False
        
        self.updateDict = {}
        for i in range(len(args)):
            #See if this args[i] needs to be uploaded to Confluence as an attachment
            if self.ALL_COLUMN_NAMES[i] in self.ATTACHMENT_COLUMN_NAMES:
                self.trace.Debug(self.ALL_COLUMN_NAMES[i], " is an attachment")
                #Upload this 'args[i]'
                #find out its contentType
                contentType = self.CONTENT_TYPE[self.ALL_COLUMN_NAMES[i]]
                if os.path.basename(args[i]) == args[i]:
                    #We assume that this 'arg' is a file present in the logs directory
                    file2Attach = os.path.join(self.logDir, args[i])
                else:
                    #Full filepath is given, so just take the args[i] as file name
                    file2Attach = args[i]
                #Attach the file to Confluence
                self.trace.Debug("calling attach", file2Attach, contentType)
                result = self.AttachFileToConfluencePage(page['id'], file2Attach, contentType)
                if result == False:
                    self.cLog("Could not atatch the file:", args[i])
                else:
                    self.cLog("Successfully attached the file:", args[i])
                
            self.updateDict[self.ALL_COLUMN_NAMES[i]] = args[i]
            
            
        #Prepare the update string
        updateString = self.PrepareUpdateString()
        
        #Update the page content
        page['content'] = self.GetUpdatedContent(page['content'], updateString)

        #Store the updated page
        try:
            page = self.server.confluence2.storePage(self.token, page)
            self.cLog('Remove automatically added page watch')
            out = self.server.confluence2.removePageWatch(self.token, page['id'])
        except Exception, e:
            self.cLogException()
            self.cLog('Error: %s' % e)
            return False
            
        self.cLog("Confluence Page updated successfully")
        return True


    def GetModifiedContent(self, content, modifiedString):
        #search for the table name in the content
        escapedTableName = re.escape(self.TABLE_NAME)
        searchPattern = '(%s.*<table>.*</table>)'%escapedTableName
        self.trace.Debug(searchPattern)
        matchObj = re.compile(searchPattern)
        if matchObj == None:
            self.cLog("matchObj is None")
            return content
        searchResults = matchObj.findall(content)
        self.trace.Debug(searchResults)
        if len(searchResults) > 0:
            self.trace.Debug("Found the table & its header")
            searchString = searchResults[0]
            searchIndex = content.find(searchString)
            #Insert the modifiedString after the searchIndex
            content = content[:searchIndex] + modifiedString + content[searchIndex + len(searchString):]
            content = content.replace("<br>", "<br/>")
            self.trace.Debug("Updated Content", content)
            return content
        else:
            self.cLog("Could not find the table")
            self.trace.Debug("Content", content)
            return content
        
        
    def ReplaceConfluencePageTable(self, newTblStr):
        try:
            #Read the config file
            self.ReadConfigFile()
        except:
            self.cLogException()
            self.cLog("Could not read config file:", self.configFile)
            return False

        #Login
        try:
            self.token = self.Login()
        except:
            self.cLogException()
            self.cLog("Could not login")
            return False

        #Get the Page
        try: 
            page = self.GetPage()
            if page == None:
                page = self.CreatePage()
            self.PAGE_ID = page['id']
        except Exception, e:
            if re.search('it does not exist', str(e)):
                self.cLog("it does not exist .. so creating the page")
                page = self.CreatePage()
                self.PAGE_ID = page['id']
        else:
            pass
           
            
        #Prepare the dictionary with the values that need to be updated to the Page
        if self.ATTACHMENT_COLUMN_NAMES != []:
            self.cLog("Cannot replace this table .. since thre are some columns which have attachments")
            return False
        
        #Update the page content
        page['content'] = self.GetModifiedContent(page['content'], newTblStr)
        #Store the updated page
        try:
            page = self.server.confluence2.storePage(self.token, page)
            self.cLog('Remove automatically added page watch')
            out = self.server.confluence2.removePageWatch(self.token, page['id'])
        except Exception, e:
            self.cLogException()
            self.cLog('Error: %s' % e)
            return False
            
        self.cLog("Confluence Page updated successfully")
        return True




if __name__ == '__main__':
    c = Confluence ("WEMO_APP_AUTOMATION_JARDEN_CONFLUENCE.cfg")
    c.ReadConfigFile()
    c.UpdateConfluencePage("","5.0.1","http://50.18.177.100/release/STAGING/WeMo-STAGING-26-13b0da4.apk","Switch, Sensor ","8689","40","21", "19", "Test Plan Document", "Html File","Logs", "", "", "", "")    
    pass
