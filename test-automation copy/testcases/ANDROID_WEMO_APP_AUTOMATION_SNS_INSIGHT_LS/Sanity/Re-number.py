import fileinput
import sys
import os
import re

pattern = '^[0-9]+\s*.'
path = os.getcwd() + "\SETUP"
pattern_obj = re.compile(pattern)
os.chdir(path)
for file in os.listdir(os.getcwd()):
    #print os.path.abspath(file)
    step_no = 0
    for line in fileinput.input(file,inplace = 1): 
        if pattern_obj.match(line):
            step_no = step_no + 1        
        print re.sub(pattern,str(step_no)+'.',line.strip())  
       #    step_no = step_no + 1          

            
        
        
        

    
    