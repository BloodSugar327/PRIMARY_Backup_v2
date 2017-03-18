import tkinter as tk
import tkinter.filedialog as fileDialog
import tkinter.messagebox as messageBox
import shlex, subprocess, shutil, os, platform, shutil2, posixpath, macpath, shlex, time
from subprocess import Popen, PIPE, STDOUT

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		self.checkSystem()
		print("\n* Select Folders to copy in GUI *")
	
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
		self.Quit = tk.Button(self, text="Quit", fg="red", command=root.destroy)
		self.Quit.pack(side="left")
		
		# Button to quit program
		self.installTagButton = tk.Button(self, text="Install Tag", fg="red", command=self.installTag)
		self.installTagButton.pack(side="left")
		
	def isTagInstalled(self):
		try:
			subprocess.run("tag -v", shell=True, check=True)
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
					
				# Print the fixed line
				print(tempString1)
				
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
					print("TAG IS INSTALLED\nCOLOR TAG COPYING SUPPORTED\n")
					print("\n* Select Folders to copy in GUI *")
					print()
					
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
		
		# Check the system version to know if color tags could be copied using TAG
		systemVersion = platform.system()
		
		global checkTag
		
		# Mac
		if systemVersion == "Darwin":
			
			# Get status of tag installation
			checkTag = self.isTagInstalled()
			
			# If tag is not installed, install it from downloaded package in root folder.
			if checkTag != True:
				
				# Call function to install tag from tagDir folder
				self.installTag()
				
			else:
				
				print("TAG IS INSTALLED\nCOLOR TAG COPYING SUPPORTED\n")
				
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
		print("FROM folder selected:\n" + src)
		
	# Initilizes global variable and stores user selected file path as the destination	
	def selectDestination_folder(self):
		global des
		des = fileDialog.askdirectory()
		print("TO folder selected:\n" + des)
		
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
		
		
	def twoFoldersChosen(self):
		
		print (src)
		if src != "":
			if des !="":
				return True
			else:
				print("You must choose TO folder.")
				return False
		else:
			print("You must choose FROM folder.")
			return False
		
		
	def progressReport(self,count,maxvalue):
		
		for x in range (0,5):  
			b = "Copying" + "." * x
			print (b, end="\r")
			time.sleep(1)
		
	
		
	# Starts the file copy process	
	def copyStart(self):
		
		
		if self.twoFoldersChosen() != True:
			return
		
		
		
		print ("Begin Copy Process")
		
		#create folder arrays
		self.initializeFolders()
		
		# Populate array with all the paths in selected source directory
		src_files = os.listdir(src)
				
		# Initialize variables for progress tracking
		i = 0
		e = len(src_files)
		
		# Start for loop with every path in array
		for file_name in src_files:
			
			#used to move though alphabet
			j = 0
				
			myFolder = ""
					
			while j < 26:
				if file_name[0] == alphabet[j]:
					print (file_name + " belongs in the " + folderName[j] + " folder")
					myFolder = folderName[j]
				j += 1
				
			print (myFolder)
			
			# The full path is the concatination of the file name and the source path
			file_name_src = os.path.join(src, file_name)
			
			# Print the full path of source
			print("Copy from: " + file_name_src)

			if myFolder != "":
				file_name_client = os.path.join(des, myFolder)
				file_name_des = os.path.join(file_name_client, file_name)
				
			else:
				# The full path is the concatination of the file name and the source path
				file_name_client = des
				file_name_des = os.path.join(file_name_client, file_name)
				

			# Print the full path of destination
			print("Copy to: " + file_name_des)
			
			if os.path.exists(file_name_des) != True:
			
				# If the path is a file
				if (os.path.isfile(file_name_src)):
					
					if os.path.exists(file_name_client) != True:
						
						os.makedirs(file_name_client)
					
					# Copy the file by itself
					print("\tCopying...\n")
					shutil2.copy2(file_name_src, file_name_des)
					

					
				# If the path is a directory
				elif (os.path.isdir(file_name_src)):
					
					# Copy the full tree
					print("\tCopying...\n")
					shutil2.copytree(file_name_src, file_name_des, isTagInstalled=checkTag)
					
				# Add 1 to progress	
				i += 1	
				
				# Calculate and Report progress to user	
				percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Copied \n")
				print(percentComplete)
			
			else:
				
				# Add 1 to progress	
				i += 1	
				
				percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Already Exists \n")
				print(percentComplete)
				
		print ("Copy Process Complete")
				
root = tk.Tk()
app = Application(master=root)
app.master.title("PRIMARY Backup Automation")
app.mainloop()