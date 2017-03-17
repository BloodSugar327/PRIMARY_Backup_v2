import tkinter as tk
import tkinter.filedialog as fileDialog
import tkinter.messagebox as messageBox
import shlex, subprocess, shutil, os, platform, shutil2, posixpath, macpath, shlex
from subprocess import Popen, PIPE, STDOUT

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		self.checkSystem()
	
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
			
			tagFile = os.path.join(tagDir,"installTag.sh")
			xcodeFile = os.path.join(fileDir,"installCommandLineTools.sh")
			
			directorytoCD = "cd " + str(tagDir)
			print(directorytoCD)
			print(tagFile)
			
#TODO: Instead if of trying to install for user, provide commands and steps necessary to install xtools and TAG

			xcodeInstall = subprocess.run(xcodeFile,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			
			
			
			if xcodeInstall.returncode == 0:
				subprocess.call(tagFile)
			elif xcodeInstall.returncode == 1:
				subprocess.call(tagFile)

			# Get status of tag installation
			checkTag = self.isTagInstalled()
			
			# If tag is not installed, install it from downloaded package in root folder.
			if checkTag != True:
				
				# Call function to install tag from tagDir folder
				self.installTag()
				
			else:
				
				print("TAG IS NOW INSTALLED")
				print("COLOR TAG COPYING SUPPORTED")
				
			return True
		except Exception:
			print("WARNING: COULD NOT INSTALL TAG \n \t COLOR TAGS WILL NOT COPY OVER")
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
				
				print("TAG IS INSTALLED")
				print("COLOR TAG COPYING SUPPORTED")
				
		# Other Systems
		else:
			
			checkTag = False
			
			# Warn user about not being able to copy that data
			print("WARNING: Copying Mac files from this system will not transfer over COLOR TAGS")
		
	# Initilizes global variable and stores user selected file path as the source
	def selectSource_folder(self):
		global src
		src = fileDialog.askdirectory()
		print(src)
		
	# Initilizes global variable and stores user selected file path as the destination	
	def selectDestination_folder(self):
		global des
		des = fileDialog.askdirectory()
		print(des)
		
		
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
		
		
	# Starts the file copy process	
	def copyStart(self):
		
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
			print(file_name_src)

			if myFolder != "":
				file_name_client = os.path.join(des, myFolder)
				file_name_des = os.path.join(file_name_client, file_name)
				
			else:
				# The full path is the concatination of the file name and the source path
				file_name_client = des
				file_name_des = os.path.join(file_name_client, file_name)
				

			# Print the full path of destination
			print(file_name_des)
			
			if os.path.exists(file_name_des) != True:
			
				# If the path is a file
				if (os.path.isfile(file_name_src)):
					
					if os.path.exists(file_name_client) != True:
						os.makedirs(file_name_client)
					
					# Copy the file by itself
					shutil2.copy2(file_name_src, file_name_des)
					
				# If the path is a directory
				elif (os.path.isdir(file_name_src)):
					
					# Copy the full tree
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