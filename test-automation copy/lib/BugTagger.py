import time, os 
import sys, traceback
import json
import glob

""" find out the parent directory of the "lib" folder .. which is 'test-automation'"""       
sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("BugTagger.py")), os.pardir)), "header"))

from Trace import *

class BugTagger():

    def __init__(self, name):
        self.trace = Trace("BugTagger.py")
        #check if the name.bugs file exists in the config folder
        self.BugFile = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("BugTagger.py")), os.pardir)), "config", name + ".bugs")
        if not os.path.exists(self.BugFile):
            self.trace.Warning("No bugs file:", self.BugFile, "... So no bugtagging is possible .. failures will just be analyzed")
            self.BugFile = None
        

    def PrepareBugDictionary(self):
        #read the bugs file and have the create a dictionary
        if self.BugFile != None and not os.path.exists(self.BugFile):
            self.trace.Warning("In PrepareBugDictionary: ", "Bugs File: %s not found!"%self.BugFile)
            self.BugFile = None

        self.KeyWords = []
        self.bugDict = {}
        if self.BugFile != None:
            bfp = open(self.BugFile, "r")
            lines = bfp.readlines()
            bfp.close()
        
            if len(lines) == 0:
                return False
            for line in lines:
                if line.find("#") == 0:
                    continue
                if "KeyWords:" in line:
                    self.KeyWords += line.split(":")[1].strip().split(";")
                elif line.find(";") > -1:
                    tCase, bugLink = line.split(";")
                    self.bugDict[tCase.strip()] = bugLink.strip()

        self.trace.Debug("self.KeyWords:", self.KeyWords)
        return True

    def AnalyzeAndTagBugs(self, logDir, csvFile):
        if not os.path.exists(os.path.join(r"%s"%logDir, csvFile)):
            raise Exception("In AnalyzeAndTagBugs: ", "Results File: %s not found in folder: %s"%(csvFile, logDir))
        fp = open(os.path.join(r"%s"%logDir, csvFile), "r")
        data = fp.read()
        fp.close()
        
        self.PrepareBugDictionary()
        
        #analisys file pointer
        afp = None
        data = data.split("\n")
        for i in range(len(data)):
            if data[i].find(",FAIL") > -1:
                #this is a failed test case .. so get its name
                tcName = data[i].split(",")[1].strip()
                #remove left parenthesis
                tcName = tcName.strip("(")
                #remove everything right from ")"
                tcName = tcName.split(")")[0].strip()
                if os.path.exists(os.path.join(logDir, tcName, tcName + ".log")):                    
                    lp = open(os.path.join(logDir, tcName, tcName + ".log"), "r")
                elif os.path.exists(os.path.join(logDir, tcName + ".log")):                    
                    lp = open(os.path.join(logDir, tcName + ".log"), "r")
                else:
                    raise Exception("In AnalyzeAndTagBugs: ", "Log File: %s not found"%tcName)
                    
                logData = lp.read()
                lp.close()
                logData = logData.split("\n")
                excList = []
                excDetail = None
                for j in range(len(logData)):
                    if logData[j].find("<--ExceptionType-->") > -1:
                        excType = logData[j].split("'")[1]
                        if excType not in excList:
                            excList.append(excType)
                            
                        if logData[j+2].find("<<<ExceptionDetails>>>") > -1 :#and logData[j+2].find("'OK'") > -1:
                            excDetail = logData[j+2].split(":")[1]
                if excList != []:
                    if afp == None:
                        afp = open(os.path.join(logDir, "ResultAnalysis.txt"), "w")
                    afp.write(tcName + ": ")
                    if excDetail != None:
                        afp.write("(" + excDetail + ") - ")
                    for e in range(len(excList)):
                        afp.write(excList[e] + ", ")
                        
                    if tcName.strip(".log") in self.bugDict:
                        afp.write("   : (" + self.bugDict[tcName.strip(".log")] + ")")
                    afp.write("\n\n")

        analysisData = ""
        if afp != None:
            afp.close()
            time.sleep(2)
            afp = open(os.path.join(logDir, "ResultAnalysis.txt"), "r")
            analysisData = afp.read()
            afp.close()
        
        return analysisData

    def AnalyzeLogFile(self, logDir, tcName):
        #analisys file pointer
        if os.path.exists(os.path.join(logDir, tcName, tcName + ".log")):                    
            lp = open(os.path.join(logDir, tcName, tcName + ".log"), "r")
        elif os.path.exists(os.path.join(logDir, tcName + ".log")):                    
            lp = open(os.path.join(logDir, tcName + ".log"), "r")
        else:
            raise Exception("In AnalyzeLogFile: ", "Log File: %s not found"%tcName)
                    
        logData = lp.read()
        lp.close()
        logData = logData.split("\n")
        excList = []
        excDetail = []
        for j in range(len(logData)):
            if logData[j].find("<--ExceptionType-->") > -1:
                excType = logData[j].split("'")[1]
                excList.append(excType)
                    
                if logData[j+2].find("<<<ExceptionDetails>>>") > -1 :
                    excDetail.append(str(logData[j+2].split("<<<ExceptionDetails>>>:")[1]))
        return excList, excDetail

        
    def AnalyzeAndTagBugs2(self, logDir, csvFile):
        if not os.path.exists(os.path.join(r"%s"%logDir, csvFile)):
            self.trace.Debug("In AnalyzeAndTagBugs2: ", "Results File: %s not found in folder: %s"%(csvFile, logDir))
            data = ""
        else:
            fp = open(os.path.join(r"%s"%logDir, csvFile), "r")
            data = fp.read()
            fp.close()
        
        self.PrepareBugDictionary()

        #analisys file pointer
        afp = None

        #Look through the console log for any suspicious messages like oom-killer, SEGV, pmortemd etc.,
        consoleLogFiles = glob.glob(os.path.join(logDir, "ConsoleLog*.txt"))
        self.trace.Debug("Console Log Files:", consoleLogFiles)
        pConsoleLogFiles = glob.glob(os.path.join(logDir, "*.pconsole.log"))
        self.trace.Debug("Pseudo Console Log Files:", pConsoleLogFiles)
        
        consoleLogFiles += pConsoleLogFiles
        for f in consoleLogFiles:
            cfp = open(f, "r")
            cfpData = cfp.read()
            truthTable = [kw in cfpData for kw in self.KeyWords]
            occurredKeyWords = [self.KeyWords[v] for v in range(len(truthTable)) if truthTable[v] == True]
            if occurredKeyWords != []:
                if afp == None:
                    afp = open(os.path.join(logDir, "ResultAnalysis.txt"), "w")
                afp.write("\nConsole Log: " + os.path.basename(f) + " contains the following KeyWords:\n\n")
                for ockw in occurredKeyWords:
                    afp.write(ockw + ", ")
                afp.write("\n\n")
        if data != "":        
            data = data.split("\n")
        else:
            data = []
            
        for i in range(len(data)):
            if data[i].find(",FAIL") > -1:
                #this is a failed test case .. so get its name
                tcName = data[i].split(",")[1].strip()
                #remove left parenthesis
                tcName = tcName.strip("(")
                #remove everything right from ")"
                tcName = tcName.split(")")[0].strip()
                lp = None
                if os.path.exists(os.path.join(logDir, tcName, tcName + ".jsonlog")):                    
                    lp = open(os.path.join(logDir, tcName, tcName + ".jsonlog"), "r")
                elif os.path.exists(os.path.join(logDir, tcName + ".jsonlog")):                    
                    lp = open(os.path.join(logDir, tcName + ".jsonlog"), "r")
                    
                logData = {}
                if lp != None:
                    logData = lp.read()
                    lp.close()
                    logData = json.loads(logData)
                excList2 = []
                for item in sorted(logData.keys()):
                    if item == "TestResult":
                        continue
                    elif item == "TestCaseFound":
                        continue
                    for subitem in sorted(logData[item].keys()):
                        #print "subitem:", subitem
                        if subitem == "DiscoveryResult":
                            #print "logData[item][subitem]:", logData[item][subitem]
                            if logData[item][subitem] == "FAILURE":
                                excList2.append("Discovery Failed for Step: " + logData[item]["Step"])
                        elif subitem == "BulbDiscoveryResult":
                            #print "logData[item][subitem]:", logData[item][subitem]
                            if logData[item][subitem] != "NA":
                                excList2.append(logData[item][subitem] + " :- for Step: " + logData[item]["Step"])
                        elif subitem == "SocketException":
                            #print "logData[item][subitem]:", logData[item][subitem]
                            if logData[item][subitem] != "NA":
                                excList2.append(logData[item][subitem] + " :- for Step: " + logData[item]["Step"])
                
                excList, excDetail = self.AnalyzeLogFile(logDir, tcName)
                if afp == None:
                    afp = open(os.path.join(logDir, "ResultAnalysis.txt"), "w")
                afp.write(tcName + ":\n\n")
                x = 0
                for x in range(len(excList2)):
                    afp.write("%d. "%(x+1) + str(excList2[x]) + "\n\n")
                for e in range(len(excList)):
                    afp.write("%d. "%(e+x+1) + str(excDetail[e]) + "\n\n")
                    
                if tcName.strip(".log") in self.bugDict:
                    afp.write("   : (" + self.bugDict[tcName.strip(".log")] + ")")
                afp.write("\n\n")
                    

        analysisData = ""
        if afp != None:
            afp.close()
            time.sleep(2)
            afp = open(os.path.join(logDir, "ResultAnalysis.txt"), "r")
            analysisData = afp.read()
            afp.close()
        
        return analysisData


    def getCloudFailLog(self, logDir, csvFile):
        if not os.path.exists(os.path.join(r"%s"%logDir, csvFile)):
            raise Exception("In AnalyzeAndTagBugs2: ", "Results File: %s not found in folder: %s"%(csvFile, logDir))
        fp = open(os.path.join(r"%s"%logDir, csvFile), "r")
        data = "".join(fp.readlines())
        fp.close()
        
        #analisys file pointer
        aStr = ""
        for line in data.split("\n"):
            if line.find("FAIL") > -1:
                #this is a failed test case .. so get its name
                
                tcName = line.split(",")[1].strip()
                #remove left parenthesis
                tcName = tcName.split("WEMO_CLOUD_TD_",1)[1]
                aStr = aStr + tcName + ": \n"
                
                if os.path.exists(os.path.join(logDir, tcName + ".log")):
                    lp = open(os.path.join(logDir, tcName + ".log"), "r")
                else:
                    raise Exception("In getCloudFailLog: ", "Log File: %s not found"%tcName)
                logData = "".join(lp.readlines())
                lp.close()
                
                
                for logLine in logData.split("\n"):
                    if logLine.find("-->FAIL<--") > -1 or logLine.find("ExceptionDetails") > -1:
                        #this is a failed test case .. so get its name
                        #print logLine
                        aStr += logLine + "\n"
                
                aStr += "\n"
        
        
        return aStr

if __name__ == '__main__':
    
    bugTagger = BugTagger("test")
    LogDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)), "logs")
    resultsCSVFile = "2015-03-23_13-50-36.csv"
    
    summaryString = ""
    analysisData = bugTagger.getCloudFailLog(LogDir, resultsCSVFile)
    if analysisData != "":
        summaryString += "\nFailed test cases:\n\n" + analysisData
    
    print summaryString

        