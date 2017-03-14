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
		self.Start = tk.Button(self, text="Start", fg="green", command=self.copyStart)
		self.Start.pack(side="left")
		
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
		
		# Start for loop with every path in array
		for file_name in src_files:
			
			# The full path is the concatination of the file name and the source path
			full_file_name = os.path.join(src, file_name)
			
			# If the path is a file
			if (os.path.isfile(full_file_name)):
				
				# Copy the file by itself
				shutil.copy2(full_file_name, des)
				
			# If the path is a directory
			elif (os.path.isdir(full_file_name)):
				
				# Copy the full tree
				shutil.copytree(src, des)
				
root = tk.Tk()
app = Application(master=root)
app.mainloop()