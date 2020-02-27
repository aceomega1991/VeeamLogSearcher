import myModules, os, threading

def mainProgram():
	while True:
		choice = input('''Welcome to the AutoMover!
Please type the option number below:\n
1.\t Move all files in the Downloads folder
2.\t Display the files in the Downloads directory\n''')
		if int(choice) == 1:
			case = input('What is the case number?')
			for file in os.listdir(myModules.path):
				myModules.fileMover(file, case)
		else:
			os.system('clear')
			if len(os.listdir()) < 1:
				print('No Files Here!')
			else:
				for file in os.listdir(myModules.path):
					print(file)
				print('\n\n')

aClear = threading.Thread(target=myModules.scheduleAutoClear)
mainApp = threading.Thread(target=mainProgram)

aClear.start()
mainApp.start()