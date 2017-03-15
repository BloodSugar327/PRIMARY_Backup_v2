import tkinter as tk
import tkinter.filedialog as fileDialog
import tkinter.messagebox as messageBox
import os
import shutil

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
	
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
		
	# Starts the file copy process	
	def copyStart(self):
		
		# Populate array with all the paths in selected source directory
		src_files = os.listdir(src)
				
		
		# Initialize variables for progress tracking
		i = 0
		e = len(src_files)
		
		# Start for loop with every path in array
		for file_name in src_files:
			
			# The full path is the concatination of the file name and the source path
			file_name_src = os.path.join(src, file_name)
			
			# Print the full path of source
			print(file_name_src)
			
			# The full path is the concatination of the file name and the source path
			file_name_des = os.path.join(des, file_name)
			
			# Print the full path of destination
			print(file_name_des)
			
			
			if os.path.exists(file_name_des) != True:
			
				# If the path is a file
				if (os.path.isfile(file_name_src)):
					
					# Copy the file by itself
					shutil.copy2(file_name_src, des)
					
				# If the path is a directory
				elif (os.path.isdir(file_name_src)):
					
					# Copy the full tree
					shutil.copytree(file_name_src, file_name_des)
					
					
				# Add 1 to progress	
				i += 1	
				
				# Calculate and Report progress to user	
				percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Copied")
				print(percentComplete)
			
			else:
				
				# Add 1 to progress	
				i += 1	
				
				percentComplete = str("{:10.2f}".format(i / e * 100) + "%" + " Complete - File Already Exists")
				print(percentComplete)
				
root = tk.Tk()
app = Application(master=root)
app.master.title("PRIMARY Backup Automation")
app.mainloop()