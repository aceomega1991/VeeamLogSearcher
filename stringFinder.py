#This script was written by Wayne Smales to parse Veeam logs faster
#This is currently ver 1.1, I plan to add more as time goes on.
#Please let me know of any bugs, you can Teams me or email me.
#Ver1.1: Fixed bug where log entries would show as filenames



import os

allFiles = []
checkedFolders = []
logFiles = []
globalPath = os.getcwd()

#Finds all files in the directory
def getfiles():    
    path = os.getcwd()
    files = os.listdir(path)
    sortedfiles = []
    for item in files:
        sort = os.path.join(os.getcwd(), item)
        if os.path.isdir(sort):
                continue
        sortedfiles.append(sort)
    return sortedfiles

#Finds all folders in the directory
def getfolders():
    path = os.getcwd()
    files = os.listdir(path)
    sorteddirs = []
    for item in files:
        sort = os.path.join(os.getcwd(), item)
        if os.path.isfile(sort):
                continue
        sorteddirs.append(sort)
    return sorteddirs

#Finds every folder recursively
def findAllFolders():
    checksum = getfolders()
    while len(checksum) != 0:
        for item in checksum:
            if item in checkedFolders:
                checksum.remove(item)
            else:
                folder = os.path.join(os.getcwd(), item)
                checkedFolders.append(folder)
                os.chdir(folder)
                findAllFolders()
    return checkedFolders

#Finds all files recursively
def findAllFiles():
    for file in os.listdir():
        if file not in allFiles:
            allFiles.append(os.path.join(os.getcwd(), file))
    for item in findAllFolders():
        os.chdir(item)
        for file in os.listdir():
            if file not in allFiles:
                allFiles.append(os.path.join(os.getcwd(), file))
            else:
                continue
    return allFiles

#Looks for the string in the name of the file
def searchNames(name):
    for file in findAllFiles():
        if name in file:
            logFiles.append(file)
    return logFiles


#Looks into all files and finds the string, pushes to a dictionary and returns this list
#By default it looks into all files with a .log extension, but can be changed to anything by setting name variable
def findStringInFile(search, name='.log'):
    errors = dict()
    for file in searchNames(name):
        if os.path.isdir(file):
            continue
        os.chdir(os.path.dirname(file))
        fileName = os.path.basename(file)
        currentFile = open(fileName, 'rb')
        for line in currentFile:
            if search in str(line):
                if fileName not in errors:
                    errors[fileName] = str(line.strip())
                else:
                    newString = errors[fileName]
                    newString += '\n' + str(line.strip())
                    errors[fileName] = newString
        currentFile.close()
    return errors

#Debug Function for finding what files program is looking at
def printNice(errorList):
    if len(errorList) != 0:
        currentName = errorList[0]
        print(currentName)
    else:
        print('Not Found in Files!')
    for item in errorList:
        if '.txt' in item:
            if currentName != item:
                 currentName = item
                 print('+' * 80)
                 print(currentName)
        else:
            print(item)

#Accepts a dictionary and writes the list to file in the same directory with name summary.txt.
#Used with the findStringInFile function.
def writeToFile(strings):
    os.chdir(globalPath)
    newFile = open('summary.log', 'a')
    newFile.write(('=' * 80) + 'Starting New Session' + ('=' * 80))
    if len(strings) != 0:
        for key in strings:
            newFile.write('\n')
            newFile.write('=' * 80)
            newFile.write('\n')
            newFile.write(key)
            newFile.write('\n')
            newFile.write('=' * 80)
            newFile.write('\n')
            newFile.write(strings[key])
    else:
        newFile.write('\nNot found in files!')
    newFile.write("\n" + ('=' * 80) + 'End Log Session' + ('=' * 80))
    newFile.close()
    print('Done')


#Convenience function for the call from main to this module
#I plan to add fuctionality as time passes
def runStringSearch(searchString, namesToLook='.log'):
    writeToFile(findStringInFile(searchString, namesToLook))

findString = input('What are we looking for today?\n')
filesToLookIn = input('If you want to search certain files, you can type what you want in here. Otherwise, leave it blank. \nDefault is to look in all .log files.\n')
if len(filesToLookIn) > 0:
    runStringSearch(str(findString), namesToLook=str(filesToLookIn))
else:
    runStringSearch(str(findString))

            




    


    
    

