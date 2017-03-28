import tkinter as tk
import tkinter.filedialog as fileDialog
import tkinter.messagebox as messageBox
import shlex, subprocess, shutil, os, platform, shutil2, posixpath, shlex, time , _thread, sys
from subprocess import Popen, PIPE, STDOUT


class bcolors:
	
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	PURPLE = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'
	HI_RED = '\033[91m'
	HI_GREEN = '\033[92m'
	HI_YELLOW = '\033[93m'
	HI_BLUE = '\033[94m'
	HI_PURPLE = '\033[95m'
	HI_CYAN = '\033[96m'
	CLEAR = '\033[K'
	BLINK = '\033[5m'

	def color(myColor):
		
		colors = [["HEADER" , '\033[95m'],
				["OKBLUE" , '\033[94m'],
				["OKGREEN" ,'\033[92m'],
				["WARNING" , '\033[93m'],
				["FAIL" , '\033[91m'],
				["END" , '\033[0m'],
				["BOLD" , '\033[1m'],
				["UNDERLINE" , '\033[4m'],
				["RED" , '\033[31m'],
				["GREEN" , '\033[32m'],
				['YELLOW' , '\033[33m'],
				["BLUE" , '\033[34m'],
				["PURPLE" , '\033[35m'],
				["CYAN" , '\033[36m'],
				["WHITE" , '\033[37m'],
				["HI_RED" , '\033[91m'],
				["HI_GREEN" , '\033[92m'],
				["HI_YELLOW" , '\033[93m'],
				['HI_BLUE' , '\033[94m'],
				["HI_PURPLE" , '\033[95m'],
				["HI_CYAN" , '\033[96m'],
				["CLEAR" , '\033[K'],
				["BLINK" , '\033[5m'],
				["Available",'\033[32m'],
				["Removed",'\033[31m'],
				["Modified",'\033[33m'],
				["Busy",'\033[34m'],
				["Failed",'\033[34m'],
				["Copied",'\033[32m'],
				["Failed Verification",'\033[31m' + '\033[4m',]]
				
		i = len(colors)
		e = 0
		while e < i:
			if myColor == colors[e][0]:
				
				return colors[e][1]
				
			e +=1

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		global monitoring
		global monitorStatus
		global stopMonitor
		global queueBusy
		global folderToMonitor
		global copyThreadDone
		os.system('cls' if os.name == 'nt' else 'clear')
		self.pack()
		self.createWidgets()
		self.checkSystem()		
		monitoring = False
		stopMonitor = False
		queueBusy = False
		copyThreadDone = False
		monitorStatus = ""
		folderToMonitor = ""
		
		print("Script Started Succesfully...\n\n* Select Folders to copy in GUI *")
	
	# Create 4 form buttons
	def createWidgets(self):
		# Button to select source folder
		self.selectSrcButton = tk.Button(self, text="Select From Folder", command=self.selectSource_folder)
		self.selectSrcButton.pack(side="left")
		
		# Button to select destination folder
		self.selectDesButton = tk.Button(self, text="Select To Folder", command=self.selectDestination_folder)
		self.selectDesButton.pack(side="left")
		
		# Button to start file copy
		global startButtonText
		startButtonText = tk.StringVar()
		self.Start = tk.Button(self, textvariable=startButtonText, fg="green", command=self.copyStart)
		self.Start.pack(side="left")
		startButtonText.set("Start")
		
		# Button to quit program
		self.Quit = tk.Button(self, text="Quit", fg="red", command=self.isDirInUse)
		self.Quit.pack(side="left")
		
		# Button to quit program
		self.installTagButton = tk.Button(self, text="Install Tag", fg="red", command=self.get_size)
		self.installTagButton.pack(side="left")
		
	def isTagInstalled(self):
		try:
			print("Tag Version: ")
			subprocess.run("tag -v", shell=True, check=True)
			print("")
			return True
		except Exception:
			return False
		
	def installTag(self):
		
		try:
			# Get file directory of script
			fileDir = os.path.dirname(os.path.realpath(__file__))
			
			# Get parent folder of script
			rootDir = os.path.split(fileDir)
			
			# Join root path with TAG folder
			tagDir = os.path.join(rootDir[0],"TAG")
			
			
			# Get the directories of files that are needed to install XCODE and TAG as dependencies
			tagFile = os.path.join(tagDir,"installTag.sh")
			xcodeFile = os.path.join(tagDir,"installCommandLineTools.sh")
			taginstructionsFile = os.path.join(fileDir,"taginstructions.txt")
		
			# Text file containing instructions to install dependencies
			textFile = open(taginstructionsFile, 'r')
			
			# Read all the lines into an array
			textLines = textFile.readlines()

			# Set variables and variable names from text files to be replaced
			pathVariables = ["\n","<xcodepath>","<tagpath>","<tagdirectory>"]
			pathUser = ["",xcodeFile,tagFile,tagDir]
			
			# Start at 0 lines
			i = 0
			
			# While we havent reached the end of the lines in file
			while i < len(textLines):
				
				# Get single line and place in temporary variable
				tempString1 = textLines[i]
					
				# Loop through the path variables that need to be replaced in text file
				for x in range(0,4):
					
					# Replace variable from tempString1 and place in secondary tempString2
					tempString2 = tempString1.replace(pathVariables[x],pathUser[x])
					
					# Give value from tempString2 to tempString1 to retain changes on loop
					tempString1 = tempString2
					
				#DEBUG: Print the fixed line
				#print(tempString1)
				
				# Move to next line
				i += 1
			
			# Variable that will wait for user to input a valid answer
			properInput = False
			
			# While the input isnt valid
			while properInput != True:
				
				# Ask user for input
				didUserInstallTag = input("Did you install TAG in system? (Y/N)").upper()
				
				# If the input is either Y/N, set properInput to True
				if didUserInstallTag =="Y":
					properInput = True
				elif didUserInstallTag =="N":
					properInput = True
			
			# If the user did install TAG succesfully
			if didUserInstallTag == "Y":

				# Get status of tag installation
				checkTag = self.isTagInstalled()
				
				# If tag is not installed, install it from downloaded package in root folder.
				if checkTag != True:
					
					# Warn user about tag status
					print("WARNING: COULD NOT FIND TAG\n\tCOLOR TAGS WILL NOT COPY OVER\n")
					print("\n* Select Folders to copy in GUI *")
					
				else:
					
					# Report succesful use of TAG
					print("TAG IS INSTALLED\n" + strColor + " TAG COPYING SUPPORTED\n")
					print("\n* Select Folders to copy in GUI *")

					
				return True
			
			# If the user chose not to install TAG	
			elif didUserInstallTag == "N":
				
				# Warn user about tag status
				print("WARNING: COPYING FILES WITHOUT TAG WILL LOSE THEIR COLOR LABEL\n")
				print("\n* Select Folders to copy in GUI *")	
				
				
		except Exception:
			
			# Warn user about tag status
			print("WARNING: COULD NOT INSTALL TAG\n\tCOLOR TAGS WILL NOT COPY OVER\n")
			print("\n* Select Folders to copy in GUI *")
			return False
		

	def checkSystem(self):
		
		global strColor
		
		strColor = bcolors.HI_RED + "C" + bcolors.HI_BLUE + "O" + bcolors.HI_GREEN + "L" + bcolors.HI_YELLOW + "O" + bcolors.HI_PURPLE + "R" + bcolors.END
		
		# Print welcome message
		print(bcolors.color("UNDERLINE") + "PRIMARY COLOR BACKUP AUTOMATION SCRIPT" + bcolors.END + "\n\nBegin Checking System...\n")
		
		
		# Check the system version to know if color tags could be copied using TAG
		systemVersion = platform.system()
		
		global checkTag
		
		# Mac
		if systemVersion == "Darwin":
			
			# Print OS Version
			print ("Running on:\nMacOS\n")
			
			# Get status of tag installation
			checkTag = self.isTagInstalled()
			
			# If tag is not installed, install it from downloaded package in root folder.
			if checkTag != True:
				
				# Call function to install tag from tagDir folder
				self.installTag()
				
			else:
				
				print("TAG IS INSTALLED\n" + strColor + " TAG COPYING SUPPORTED\n")
				
		# Other Systems
		else:
			
			checkTag = False
			
			# Warn user about not being able to copy that data
			print("WARNING: Copying Mac files from this system will not transfer over COLOR TAGS")
			
		# Initialize 2 global variables that will hold the source and destination paths
		global src
		global des
		
		src = ""
		des = ""
		
	# Initilizes global variable and stores user selected file path as the source
	def selectSource_folder(self):
		global src
		src = fileDialog.askdirectory()
		print("\nFROM folder selected:\n" + bcolors.BOLD	+ src + bcolors.END)
		
	# Initilizes global variable and stores user selected file path as the destination	
	def selectDestination_folder(self):
		global des
		des = fileDialog.askdirectory()
		print("\nTO folder selected:\n" + bcolors.BOLD	+ des + bcolors.END)
		
	def initializeFolders(self):
		
		global alphabet
		global folderName
		
		alphabet = []
		folderName = []
		
		f = 65
		
		while f < 91:
			alphabet.append(chr(f))
			folderName.append(str(chr(f)) + "-Clients")
			
			f += 1
		
		#print(alphabet)
		#print(folderName)
		
	def getClientFolder(self,fileName):
		
		#used to move though alphabet
		j = 0
			
		myFolder = ""
				
		while j < 26:
			if fileName[0].upper() == alphabet[j]:
				#print (fileName + " belongs in the " + folderName[j] + " folder")
				return folderName[j]
			j += 1
		
		
	def twoFoldersChosen(self):
	
		if src != "":
			if des !="":
				return True
			else:
				print("You must choose TO folder.")
				return False
		else:
			print("You must choose FROM folder.")
			return False
		
	def progressReport(self,message,delay):

		for x in range (0,4):  
			print(bcolors.CLEAR, end="\r") 
			b = str(message) + "." * x
			print (b, end="\r")
			time.sleep(delay)


	def printReport(self):
		
		i = len(allFiles)
		e = 0
		
		while e < i:
			
			print(str(allFiles[e][0]) + " - " + str(allFiles[e][1]) + " - " + str(allFiles[e][2]) + " - " + str(allFiles[e][3]))
			
			e += 1
		
	def printList(self):
			
		print("Files remaining to copy: \n")
		i = 0
		while i < len(availableFiles):
			print(availableFiles[i])
			i += 1
		
		i = 0
		print("\n")
	
		print("Files modified while copying: \n")
		while i < len(modifiedFiles):
			print(modifiedFiles[i])
			i += 1
	
		i = 0
		print("\n")
		print("Files deleted while copying: \n")
		while i < len(deletedFiles):
			print(deletedFiles[i])
			i += 1
		
	def verifyFiles(self,source,destination):
	
		print("\tVerifying...")
	
		sourceFile = self.get_size(source)
		destinationFile = self.get_size(destination)
		
		sourceStats = os.stat(source)
		destinationStats = os.stat(destination)
		
		if sourceFile == destinationFile:
			if sourceStats.st_mtime == destinationStats.st_mtime:
				return True
			else:
				return False
		else:
			return False
	
	# Starts the file copy process	
	def copyStart(self):
		
		# To stop monitor once process completes
		global stopMonitor
		
		# used to store and report copiedFiled
		global copiedFiles
		
		global allFiles
		
		# Used to report why file copy may have failed
		failCode = 0
		
		# Don't start if two folders havent been chosed
		if self.twoFoldersChosen() != True:
			return
		
		# Let used know process has begun
		print("\nBegin Copy Process...\n")
		
		# Begin monitoring files in source folder
		self.startMonitoring()
		
		stopMonitor = False
		
		while monitoring != True:
			self.progressReport("Waiting for file monitor to start" + "(" + str(monitorStatus) + ")",.5)
				
		print(bcolors.BLINK + "\n\nFILE MONITOR STARTED!\n" + bcolors.END)
		
		#create folder arrays
		self.initializeFolders()
				
		# Initialize variables for progress tracking
		i = 0
		e = len(allFiles)
		
		#Get first file
		#file_name = self.getFile(availableFiles)
		
		theFile = self.getFile2("Available")
		
		file_name = theFile[1]
		
		print("Fetching from queue...\n")
		
		print("Got file " + bcolors.BOLD + str(file_name) + bcolors.END + " from queue:\n")
		
		# Start while loop until you can't receive any more files.
		while file_name != "":
			
			myFolder = self.getClientFolder(file_name)
					
			print ("\t" + bcolors.BOLD + file_name + bcolors.END + " belongs in the " + bcolors.BOLD + myFolder + bcolors.END + " folder")

			# The full path is the concatination of the file name and the source path
			file_name_src = os.path.join(src, file_name)
			
			
			# Set the destination folder depending on file's first initial
			if myFolder != "":
				
				
				file_name_client = os.path.join(des, myFolder)
				file_name_des = os.path.join(file_name_client, file_name)
				
			else:
				
				# The full path is the concatination of the file name and the source path
				file_name_client = des
				file_name_des = os.path.join(file_name_client, file_name)
				
			# Print the full path of source
			print("\tCopy from: " + file_name_src)
				
			# Print the full path of destination
			print("\tCopy to: " + file_name_des)
			
			# Set and initialize boolean that will keep track of copying
			copiedSuccesfully = False
			
			
			# Begin Copy Procedure
			if os.path.exists(file_name_des) != True:
			
				# If the path is a file
				if (os.path.isfile(file_name_src)):
					
					if os.path.exists(file_name_client) != True:

						os.makedirs(file_name_client)
					
					# Copy the file by itself
					print("\tCopying...\n")
					
					try:
					
						shutil2.copy2(file_name_src, file_name_des)
						copiedSuccesfully = True
						
					except:
						
						failCode = 2
						
						copiedSuccesfully = False
					
					#if copiedAvailableBytes == True:
						
						# Verify all bytes have been written
							#TODO: Write code to handle verification of a single file
					
				# If the path is a directory
				elif (os.path.isdir(file_name_src)):
					
					currentFolderSize = self.get_size(file_name_src)
					
					if currentFolderSize == theFile[2]:

						dirAvail = self.isDirInUse(start_path=file_name_src,printResults=True,stream=False,pollTime=10)
						
						if dirAvail != True:				
							# Copy the full tree
							print("\r\tCopying...")
							
							try:
							
								shutil2.copytree(file_name_src, file_name_des, isTagInstalled=checkTag)
								copiedSuccesfully = True
								
							except:
								
								failCode = 0
								
								copiedSuccesfully = False
								
						else:
							
							failCode = 1
							
							copiedSuccesfully = False
							
					else:
						
						failCode = 2
						
						copiedSuccesfully = False
											
				# Add 1 to progress	
				i += 1	
				
				#Reporting
				
				if copiedSuccesfully == True:
				
					# Verify file size is the same
					filePass = self.verifyFiles(file_name_src,file_name_des)
					
					if filePass == True:
													
						# Calculate and Report progress to user	
						percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Copied \n")
						theFile = (theFile[0],theFile[1],theFile[2],"Copied")
						print(bcolors.GREEN + percentComplete + bcolors.END)
						
					else:
						
						# Add file to modified array
						self.modifiedInQueue([file_name])
						
						# Calculate and Report progress to user	
						percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Verification Failed \n")
						theFile = (theFile[0],theFile[1],theFile[2],"Failed Verification")
						print(bcolors.YELLOW + percentComplete + bcolors.END)
						
				else:
					
					#TODO: Add if statements for Failcode variables
					
					# Calculate and Report progress to user
					
					if failCode == 0:
				
						percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Copying Failed \n")
						theFile = (theFile[0],theFile[1],theFile[2],"Failed")
						print(bcolors.RED + percentComplete + bcolors.END)
					
					elif failCode == 1:
					
						percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File In Use, Will Try Again Later \n")
						theFile = (theFile[0],theFile[1],theFile[2],"Busy")
						print(bcolors.YELLOW + percentComplete + bcolors.END)
						
					elif failCode == 2:
					
						percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Modified During Copy Process \n")
						theFile = (theFile[0],theFile[1],theFile[2],"Modified")
						print(bcolors.YELLOW + percentComplete + bcolors.END)
	
			
			else:
				
				# Add 1 to progress	
				i += 1	
				
				percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Already Exists \n")
				theFile = (theFile[0],theFile[1],theFile[2],"Not Copied")
				print(bcolors.YELLOW + percentComplete + bcolors.END)
					
			
			fileIndex = theFile[0]
			
			allFiles[fileIndex] = theFile
			
			theFile = self.getFile2("Available")
			
			if theFile != "":
				
				file_name = theFile[1]
				
				print("Got file " + str(file_name) + " from queue:\n")
				
						
			else:
				
				while queueBusy:
					
					self.progressReport("Waiting for file",.5)
					
					
				theFile = self.getFile2("Available")
				
				if theFile != "":
					
					file_name = theFile[1]
					
					print("Got file " + str(file_name) + " from queue:\n")
				
				else:
				
					busyCount = self.countQueue("Busy")
					modifiedCount = self.countQueue("Modified")
					failedCount = self.countQueue("Failed")
					copiedCount = self.countQueue("Copied")
	
					answer = input("There are no files available to copy,\nWould you like to check if Busy files are available now?")
					
					if answer == "Y":
						
						self.checkQueue()
						
						theFile = self.getFile2("Available")
							
						if theFile != "":
							
							file_name = theFile[1]
							
							print("Got file " + str(file_name) + " from queue:\n")
							
						else:
							
							file_name = ""	
						
					else:
					
						file_name = ""	
		
				
		stopMonitor = True
		
		time.sleep(5)
				
		print ("Copy Process Complete\n")
		
		self.printReport()
		
	# Define a function for the thread
	def print_time(self, threadName, delay):
		count = 0
		while count < 5:
			time.sleep(delay)
			count += 1
			print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
	
	def files_to_timestamp(self,path):
		files = [os.path.join(path, f) for f in os.listdir(path)]
		return dict ([(f, os.path.getmtime(f)) for f in files])
	
	def get_size(self,start_path = '.'):
			
			total_size = 0
			for dirpath, dirnames, filenames in os.walk(start_path):
				for f in filenames:
					fp = os.path.join(dirpath, f)
					total_size += os.path.getsize(fp)
					
			
			return total_size
			
			
	def copyInThread(self,src,des,IsADir):
		
		
		if IsADir:
			
			shutil2.copytree(src, des, isTagInstalled=checkTag)
			
		else:
			
			shutil2.copy2(src, des)
		
	def incrementType(self,stream):
		
		i = len(stream)
		e = 0
		
		increasing = 0
		fixed = 0
		decreasing = 0
		
		topNumber = stream[e]
			
		e += 1
		
		while e < i:
			nextNumber = stream[e]
			
			if topNumber == nextNumber:
				fixed += 1
			elif topNumber > nextNumber:
				decreasing += 1
			elif topNumber < nextNumber:
				increasing += 1
				
			topNumber = nextNumber
				
			e += 1
					
		increasingPercent = increasing/(i-1) * 100
		fixedPercent = fixed/(i-1) * 100
		decreasingPercent = decreasing/(i-1) * 100
				
		results = [
				("Increasing", increasingPercent, increasing),
				("Fixed", fixedPercent, fixed),
				("Decreasing", decreasingPercent, decreasing),
		]
				
		resultsSorted = sorted(results,key=lambda type: type[2],reverse=True)
		
		topResult = resultsSorted[0]
		
		return topResult
		
	def getFile2(self, fromQueue):
		
		global allFiles
		global queueBusy
		
		gotFile = False
		
		fileToReturn = ""
		
		while gotFile == False:
			
			if queueBusy == False:
				
				i = len(allFiles)
				
				if i > 0:
					
					e = 0
					
					while e < i:		
						currentFile = allFiles[i-1]							
						if currentFile[3] == fromQueue:
							#print(currentFile)
							fileToReturn = currentFile
							gotFile = True
							
						i -= 1
						
					if gotFile == False:
						fileToReturn = ""
						gotFile = True
			else:
				self.progressReport("Waiting for file",.5)
					
						
					
		if gotFile == True:
			
			return fileToReturn
		else:
			return ""
		
	def countQueue(self,queueToCount):
		
		i = len(allFiles)
		count = 0
		
		e = 0
		
		while e < i:
			currentFile = allFiles[e]	
			if currentFile[3] == queueToCount:
				count += 1
			
			e += 1
			
		return count
		
		
	def addToQueue(self,itemsToAdd):
		
		global allFiles
	
		i = len(itemsToAdd)
		e = 0
		
		foundIt = False
		
		while e < i:
			
			fileName = os.path.basename(itemsToAdd[e])
			
			if fileName != ".DS_Store":
			
				f = len(allFiles)
				g = 0
				
				while g < f:
					
					currentFile = allFiles[g]
					
					if currentFile[1] == itemsToAdd[e]:
						
						fileIndex = currentFile[0]
						
						newFile = (currentFile[0],currentFile[1],currentFile[2],"Available")
						
						allFiles[fileIndex] = newFile
						
						foundIt = True
						
						#print ("\t" + bcolors.BLUE + "Added: " + fileName + bcolors.END)
						
					g += 1
						
				if foundIt != True:
										
					fileName = os.path.basename(itemsToAdd[e])
					
					filePath = os.path.join(src,itemsToAdd[e])
					fileSize = self.get_size(filePath)
					fileStat = self.isDirInUse(start_path=filePath, printResults= False,stream=False, pollTime = 5)
					
					slotNumber = len(allFiles)
				
					if fileStat:
					
						fileInUse = "Busy"
						
					else:
						
						if fileSize > 0:
						
							fileInUse = "Available"
						else:
							fileInUse = "Busy"
						
					allFiles.append((slotNumber,fileName,fileSize,fileInUse))
					
					#print ("\t" + bcolors.color(fileInUse) + str(fileInUse) + ": "+ str(fileName) + bcolors.END)
					
			
			e += 1
			
			
	def updateItem(self,fileName,fileSlot = 0,fileSize =0,fileStat=""):
		
		global allFiles
		
		i = len(allFiles)
		e = 0
		
		found = False
		
		while e < i:
			
			currentItem = allFiles[e]
			
			if currentItem[1] == fileName:
				#Collect initial data, if empty in function
				
				if fileSlot == 0:
					fileSlot = currentItem[0]
				if fileSize == 0:
					fileSize = currentItem[2]
				if fileStat == "":
					fileStat = currentItem[3]
					
				found = True
			
			e += 1
		
		
		if found:
				
			newItem = (fileSlot,fileName,fileSize,fileStat)
			
			allFiles[fileSlot] = newItem
				
			#print ("\t" + bcolors.color(fileStat) + fileStat + ":" + fileName + bcolors.END)
			
		#else:
			
			#print ("\t" + bcolors.RED + "Failed to update status: " + fileName + bcolors.END)
		
		
	def removeFromQueue(self,itemsToRemove):

		i = 0
		
		while i < len(itemsToRemove):
			
			
			fileName = os.path.basename(itemsToRemove[i])
			
			if fileName != ".DS_Store":
			
				self.updateItem(fileName, fileStat="Removed")
					
			
			i += 1

		
	def modifiedInQueue(self,itemsModified):
	
		i = 0
		
		while i < len(itemsModified):
			
			
			fileName = os.path.basename(itemsModified[i])
			
			if fileName != ".DS_Store":
			
				self.updateItem(fileName, fileStat="Modified")
					
			
			i += 1

		
	def checkQueue(self):
		
		
		filesToCheck = allFiles
		
		i = len (filesToCheck)
		e = 0
		
		while e < i:
			
			currentFile = filesToCheck[e]
			
			filePath = os.path.join(src,currentFile[1])
			if currentFile[3] != "Available":
				if currentFile[3] != "Copied":
					if os.path.exists(filePath):
						if os.path.isdir(filePath):
							if self.isDirInUse(filePath) == False:
								queueBusy = True
								currentSize = self.get_size(filePath)
								self.updateItem(fileName=currentFile[1],fileSize=currentSize,fileStat="Available")
								queueBusy = False
					else:
						queueBusy = True
						self.updateItem(fileName=currentFile[1],fileStat="Removed")
						queueBusy = False
			e += 1
	
	
	def isDirInUse(self,start_path = '.', printResults= True,stream= False, pollTime = 5):
	
		t_end = time.time() + pollTime
		
		sizeOfFile = []
		if stream ==True:

			print(start_path)
		
		while time.time() < t_end:
			
			size = self.get_size(start_path)
			
			sizeOfFile.append(size)
			
			if stream ==True:
				
				print(size)
			
			if printResults==True:
				
				self.progressReport("\tPolling",.5)
			else:
				
				time.sleep(.5)
	
		dirIncrement = self.incrementType(sizeOfFile)
				
		if stream==True:

			print(dirIncrement)
		
		if dirIncrement[0] == "Fixed":
			
			if printResults==True:
				
				print("\n\tDirectory not in use")
				
			return False
			
		else:
			
			if printResults==True:
				
				print("\n\tDirectory is in use")
				
			return True
					
				
	def checkAllFiles(self,src,arrayOfFiles):
		
		global monitorStatus
		
		i = len(arrayOfFiles)
		e = 0
		
		filesToReturn = []
		
		while e < i:
			
			if arrayOfFiles[e] != ".DS_Store":

				fileName = arrayOfFiles[e]
				filePath = os.path.join(src,arrayOfFiles[e])
				fileSize = self.get_size(filePath)
				
				
				if self.isDirInUse(filePath, printResults= False, pollTime = 6):
				
					fileInUse = "Busy"
					
				else:
					fileInUse = "Available"
				
				
				filesToReturn.append((e-1,fileName,fileSize,fileInUse))
			
			e += 1
		
			monitorStatus = "Checking all files - " + str(e/i*100) + "%"
		
		return filesToReturn
		
	def startMonitoring(self):
		
		# Create new thread
		try:
			
			_thread.start_new_thread(self.fileMonitor, (src, 2, ) )
			
		except:
			
			print ("Error: unable to start thread")
		
				
	def fileMonitor(self,srcToWatch, delay):
		
		global monitoring
		global monitorStatus
		global allFiles
		global filesChecked
		global queueBusy
		
		filesChecked = False
		
		monitorStatus = "Started"
		
		path_to_watch = os.path.abspath(srcToWatch)
	
		availableFiles = os.listdir(srcToWatch)
				
		#DEBUG: Used to view available files in folder so far
		#print(availableFiles)

		before = self.files_to_timestamp(path_to_watch)
		
		print ("Watch Start:" + path_to_watch + "\n")
		
		while stopMonitor != True:
			
			if filesChecked ==False:
				
				monitorStatus = "Checking all files"
				
				allFiles = self.checkAllFiles(srcToWatch, availableFiles)
				
				monitorStatus = "All files checked"
				
				print("\n\n")
				
				filesChecked = True
				
				monitoring = True
				
				time.sleep(delay*4)
				
			after = self.files_to_timestamp(path_to_watch)
			added = [f for f in after.keys() if not f in before.keys()]
			removed = [f for f in before.keys() if not f in after.keys()]
			modified = []
		
			for f in before.keys():
				if not f in removed:
					if os.path.getmtime(f) != before.get(f):
						modified.append(f)
						
			queueBusy = True
			if added:
				self.addToQueue(added)
			if removed:
				self.removeFromQueue(removed)
			if modified: 
				self.modifiedInQueue(modified)
			queueBusy = False

			
			time.sleep (delay)
			
			before = after
		
		
		print ("Watch End: " + path_to_watch + "\n")
		
		monitoring = False
			
				
root = tk.Tk()
app = Application(master=root)
app.master.title("PRIMARY Backup Automation")
app.mainloop()