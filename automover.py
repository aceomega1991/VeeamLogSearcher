from pyunpack import Archive
from pathlib import Path
import os, zipfile, shutil, traceback, time, schedule, threading, re


path = str(os.path.join(Path.home(), 'Downloads'))
destination = str(os.path.join(Path.home(), 'Documents'))

def automover():
	global path, destination
	os.chdir(path)
	while True:
		try:
			if len(checkFiles(path)) >= 1:
				for file in checkFiles(path):
					print('File Found: {}'.format(file))
				case = input('Case Number?\n')
				os.system('cls')
				checkProgress(path)
				endpath = os.path.join(destination, case)
				if not os.path.isdir(endpath):
					os.mkdir(endpath)
				for file in checkFiles(path):
					if zipfile.is_zipfile(file):
						newPath = uniquePath(endpath, os.path.splitext(file)[0])
						Archive(file).extractall(newPath, auto_create_dir=True)
						os.remove(file)
					else:
						shutil.move(file, os.path.join(endpath, file))
			else:
				time.sleep(5)
		except Exception:
			traceback.print_exc()

def autoClear():
	global destination
	os.chdir(destination)
	folders = os.listdir()
	configFile = os.path.join(destination, 'Closed.txt')
	if not os.path.isfile(configFile):
		with open(configFile, 'w+') as create:
			pass
	with open(configFile, 'r+') as read:
		for line in read.readlines():
			stripLine = line.replace('\n', '')
			if stripLine in folders:
				shutil.rmtree(line)
	os.remove(configFile)
	with open(configFile, 'w+') as create:
		pass


def scheduleAutoClear():
	schedule.every().day.at('22:00').do(autoClear)
	while True:
		schedule.run_pending()
		time.sleep(1)


def checkFiles(directory):
	fileList = []
	for file in os.listdir(directory):
		if file == 'desktop.ini':
			continue
		else:
			fileList.append(file)
	return fileList

def checkProgress(directory):
	sep = ' '
	fileString = sep.join(checkFiles(directory))
	while re.match(r'.+\.part', fileString):
		time.sleep(3)
		fileString = sep.join(checkFiles(directory))

def uniquePath(directory, filename):
	i = 1
	oldPath = os.path.splitext(filename)[0]
	while os.path.exists(os.path.join(directory, oldPath)):
		oldPath = os.path.splitext(filename)[0] + '({})'.format(i)
		i = i + 1
	return os.path.join(directory, oldPath)




aClear = threading.Thread(target=scheduleAutoClear)
aMover = threading.Thread(target=automover)

aClear.start()
aMover.start()