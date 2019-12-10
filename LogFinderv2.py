#This is the second version on the log finder for Veeam Software Logs
#Use at your own risk, this code is maintained by Wayne Smales
#This update makes the code more modular and allows for customization
import os

debug = false
debugLog = []
taskLog = {}
vmcLog = {}
jobLog = {}
sourceLog = {}
targetLog = {}
otherLog = {}
taskSearch = []
vmcSearch = []
jobSearch = []
sourceSearch = []
targetSearch = []
otherSearch = []
path = ''











def loadLogs():
    if global debug:
        global debugLog.append('Hello from the log loading!')
    global path = os.getcwd()
    for root, dirs, files in os.walk():
        for name in files:
            pathName = os.path.join(root, name)
            if 'task' in name:
                global taskLog[name] = pathName
            elif 'VMC' in name:
                global vmcLog[name] = pathName
            elif 'job' in name:
                global jobLog[name] = pathName
            elif 'source' in name:
                global sourceLog[name] = pathName
            elif 'target' in name:
                global targetLog[name] = pathName
            else:
                global otherLog[name] = pathName
    if global debug:
        global debugLog.append('Log load complete!')

def loadConfig(customPage):
    for item in os.listdir(os.getcwd()):
        if customPage in item:
            if item.is_file():
                with open(customPage, 'r') as configPage:
                    for line in configPage:
                        if load == False:
                            if '!' in line:
                                if 'task' in line:
                                    continue
                                elif 'VMC' in line:
                                    vmcbool = True
                                    taskbool = False
                                    continue
                                elif 'job' in line:
                                    continue
                                    while '!' not in line:
                                    jobSearch.append(line)
                                elif 'source' in name:
                                    continue
                                    while '!' not in line:
                                        taskSearch.append(line)
                                elif 'target' in line:
                                    continue
                                    while '!' not in line:
                                    targetSearch.append(line)
                                else:
                                global otherLog[name] = pathName
                        
    
                
    
