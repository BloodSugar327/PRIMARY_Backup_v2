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

	def createWidgets(self):
		self.selectSrcButton = tk.Button(self, text="Select From Folder", command=self.selectSource_folder)
		self.selectSrcButton.pack(side="left")
		
		self.selectDesButton = tk.Button(self, text="Select To Folder", command=self.selectDestination_folder)
		self.selectDesButton.pack(side="left")
		
		self.Start = tk.Button(self, text="Start", fg="green", command=self.copyStart)
		self.Start.pack(side="left")
		
		self.Quit = tk.Button(self, text="Quit", fg="red", command=root.destroy)
		self.Quit.pack(side="left")

	def selectSource_folder(self):
		global src
		src = fileDialog.askdirectory()
		print(src)
		
	def selectDestination_folder(self):
		global des
		des = fileDialog.askdirectory()
		print(des)
	def copyStart(self):
		print (des)
		x = 0
		src_files = os.listdir(src)
		for file_name in src_files:
			x = x + 1
			print(x) 
			full_file_name = os.path.join(src, file_name)
			if (os.path.isfile(full_file_name)):
				shutil.copy2(full_file_name, des)
				
root = tk.Tk()
app = Application(master=root)
app.mainloop()