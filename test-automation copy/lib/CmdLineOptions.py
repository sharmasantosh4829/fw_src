import time, os 
import sys, traceback
from optparse import OptionParser

""" find out the parent directory of the "lib" folder .. which is 'automation'"""       
sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("CmdLineOptions.py")), os.pardir)), "header"))

from Trace import *

def _loadCmdOptionsDefaults(self):
    #read the default values of different command line options from the file "OptionsFile" in the config folder
    if not os.path.exists(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("CmdLineOptions.py")), os.pardir)), "config", self.OptionsFile)):
        self.trace.Critical("No OptionsFile:", self.OptionsFile)
        return False
    fp = open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("CmdLineOptions.py")), os.pardir)), "config", self.OptionsFile), "r")
    lines = fp.readlines()
    fp.close()
    
    if len(lines) == 0:
        return False
    for line in lines:
        #skip comments and blank lines
        if line.find("#") == 0 or line.strip() == "":
            continue
        if line.find(";") > -1:
            parameter = line.split(";")
            if parameter[1] == "bool":
                if parameter[2] == "false":
                    self.cmdParser.add_option("--%s"%parameter[0], action = "store_true", dest = "%s"%parameter[0],default = False, help = '%s'%parameter[3].strip())
                elif parameter[2] == "true":
                    self.cmdParser.add_option("--%s"%parameter[0], action = "store_false", dest = "%s"%parameter[0],default = True, help = '%s'%parameter[3].strip())
                else:
                    self.trace.Critical("Syntax error in line", line, "in ", self.OptionsFile)
                    return False
            elif parameter[1] == "int" or parameter[1] == "integer":
                self.cmdParser.add_option("--%s"%parameter[0], type = "int", action = "store", dest = "%s"%parameter[0],default = "%s"%parameter[2], help = '%s'%parameter[3].strip())
            else:
                self.cmdParser.add_option("--%s"%parameter[0], action = "store", dest = "%s"%parameter[0],default = "%s"%parameter[2], help = '%s'%parameter[3].strip())
        else:
            self.trace.Critical("Syntax error in", self.OptionsFile)
            return False
    
    return True


class CmdLineOptions():

    # ====================================================
    def __init__(self, **arguments):
        self.trace = Trace("CmdLineOptions.py")
        self.OptionsFile = ""
        self.cmdParser = OptionParser()
        
        if 'OptionsFile' in arguments:
            ''' This OptionsFile must exist in the 'config' folder '''
            self.OptionsFile = arguments['OptionsFile']
            #read the OptionsFile and parse
            _loadCmdOptionsDefaults(self)
            (self.options, self.cmdArgs) = self.cmdParser.parse_args()
            self.trace.Debug("cmdOptions", self.options)
            self.trace.Debug("cmdArgs", self.cmdArgs)
            
        else:
            #If no OptionsFile is given
            self.options = {}
            self.cmdArgs = []
            self.trace.Debug("cmdOptions", self.options)
            self.trace.Debug("cmdArgs", self.cmdArgs)


if __name__ == '__main__':
    obj = CmdLineOptions(OptionsFile = "WeMoCloudApiTestDevice.options")


        