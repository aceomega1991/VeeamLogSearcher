#This code is written and maintained by Wayne Smales for Veeam Software Corporation
#This is a remade code and will be updated whenever I decide to stop procrastinating
#All request for functionality can be submitted to wayne.smales@veeam.com


import os
import sqlite3


def getFiles(path=os.getcwd()):
    fileList = []
    for root, dirs, files in os.walk(path):
        for name in files:
            fileList.append([os.path.join(root, name)])
    return fileList


def sortFiles(fileList):
    for file in fileList:
        if 'task' in file.lower():
            addToFilesDB(file, 'task')
        if 'job' in file.lower:
            addToFilesDB(file, 'job')
        if 'source' in file.lower:
            addToFilesDB(file, 'source')
        if 'target' in file.lower:
            addToFilesDB(file, 'target')
        if 'vmc' in file.lower:
            addToFilesDB(file, 'vmc')

def writeToSummary(itemToWrite, path = 'summary.log', delimitor = '\n'):
    with open(path, 'a') as summaryOut:
        summaryOut.write(str(itemToWrite) + delimitor)

def readFromFiles(pathName, *searchterm):
    with open(pathName, 'r') as openFile:
        for item in searchterm:
            for line in openFile.readline():
                if item in line:
                    pass
                #Add it to DB as possible
                else:
                    continue

def initiateDB():
    with sqlite3.connect(os.path.join(os.getcwd(), 'tempDB.db')) as conn:
        sqlCurs = conn.cursor()
        addedDB = [('job'), ('task'), ('source'), ('target'), ('vmc')]
        for i in range(len(addedDB)):
            dbInitiate = '''
            CREATE TABLE IF NOT EXISTS {}
            (
            fileName TEXT NOT NULL
            );
            '''.format(addedDB[i])

            sqlCurs.execute(dbInitiate)


def addToFilesDB(fileToAdd, table='filenames'):
    with sqlite3.connect(os.path.join(os.getcwd(), 'tempDB.db')) as conn:
        sqlCurs = conn.cursor()
        addData = 'INSERT INTO {}(fileName) VALUES(?);'.format(table)
        sqlCurs.executemany(addData, fileToAdd)
        conn.commit()


def printFiles( table, column='fileName'):
    with sqlite3.connect(os.path.join(os.getcwd(), 'tempDB.db')) as conn:
        sqlCurs = conn.cursor()
        getData = 'SELECT {} FROM {}'.format(column, table)
        sqlCurs.execute(getData)
        rows = sqlCurs.fetchall()
        filesSearched = 0
        for row in rows:
            print(row)
            writeToSummary(row)
            filesSearched += 1
        print(filesSearched)


def removeDB(path=os.path.join(os.getcwd(), 'tempDB.db')):
    if os.path.exists(path):
        os.remove(path)



initiateDB()
addToFilesDB(getFiles(), 'task')
printFiles('task')
removeDB()









