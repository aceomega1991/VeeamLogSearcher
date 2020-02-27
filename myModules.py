from pyunpack import Archive
from pathlib import Path
import os, time, shutil, threading, zipfile, schedule


path = str(os.path.join(Path.home(), 'Downloads'))
destination = str(os.path.join(Path.home(), 'Documents'))

def fileList(path):
	with open(path, 'r') as file:
		formatList = [case.splitlines() for case in file.readlines()]
		[''.join(case.split()) for case in formatList]
	return formatList


def testFileAccess(fileName):
	try:
		os.rename(fileName, fileName)
	except Exception as e:
		print('File Not ready')
		time.sleep(1)
		testFileAccess(fileName)


def autoClear():
	os.chdir(destination)
	folders = os.listdir()
	configFile = os.path.join(destination, 'Closed.txt')
	if not os.path.isfile(configFile):
		with open(configFile, 'w+') as create:
			pass
	[shutil.rmtree(case) for case in fileList(configFile) if case in folders]
	os.remove(configFile)
	with open(configFile, 'w+') as create:
		pass


def checkFiles(directory):
	fileList = []
	for file in os.listdir(directory):
		if file == 'desktop.ini':
			continue
		else:
			fileList.append(file)
	return fileList


def uniquePath(directory, filename):
	i = 1
	oldPath = os.path.splitext(filename)[0]
	while os.path.exists(os.path.join(directory, oldPath)):
		oldPath = os.path.splitext(filename)[0] + '({})'.format(i)
		i = i + 1
	return os.path.join(directory, oldPath)


def fileMover(dFile, case):
	os.chdir(path)
	while True:
		try:
			testFileAccess(dFile)
			break
		except Exception:
			time.sleep(1)
	endpath = os.path.join(destination, case)
	if not os.path.isdir(endpath):
		os.mkdir(endpath)
	if file in checkFiles(path):
		if zipfile.is_zipfile(file):
			newPath = uniquePath(endpath, os.path.splitext(file)[0])
			Archive(file).extractall(newPath, auto_create_dir=True)
			os.remove(file)
		else:
			shutil.move(file, os.path.join(endpath, file))
	else:
		print('File not found!')


def scheduleAutoClear():
	schedule.every().day.at('22:00').do(autoClear)
	while True:
		schedule.run_pending()
		time.sleep(1)


