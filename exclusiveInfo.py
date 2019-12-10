import stringFinder, re, os






#This will take an input and search a file for all lines that contain that input.
#Returns a list object
def findItem(logName, item):
    names = stringFinder.searchNames(logName)
    if len(names) == 0:
        print('Cannot find the expected log: ' + logName)
    else:
        for file in names:
            if os.path.isdir(file):
                continue
            os.chdir(os.path.dirname(file))
            fileName = os.path.basename(file)
            currentFile = open(fileName, 'rb')
            for line in currentFile:
                if item in line:
                    matches.append(line)
    return matches
                
    

