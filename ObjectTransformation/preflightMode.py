from Tkinter import *
import ttk
from tkColorChooser import askcolor
import tkFileDialog

class PreFlightMode(Frame) :
	"""
	Pre-flight Mode
	"""
	
	# colour variables
	colour_background = "#3b98e3"
	colour_breadcrumbs = "#135e1c"
	colour_flightlines = "#ffff33"
	colour_ramps = "#ff0000"

	displayColorBackground = None
	displayColorBreadcrumbs = None
	displayColorFlightlines = None
	displayColorRamps = None

	displayWeightFlightlines = None
	displayWeightBreadcrumbs = None

	displayFileFlightlines = None
	displayFileFlightramps = None

	# weight variables
	weight_breadcrumbs = 5
	weight_flightplan = 2

	# file selector to get paths of files
	# user selects both flightlines file and ramps file
	filepath_flightlines = None
	filepath_ramps = None

	listening = None

	root = None

	def __init__( self, master, listening ) :
		Frame.__init__(self, master)
		if (master is None): 
			master = self
		self.root = master
		self.pack()
		self.listening = listening
		self.initWindow()


	def initWindow(self): 
		colorSelectionArea = self.initColorSelectionArea(self.root)
		colorSelectionArea.pack(ipady = 3)

		weightSelectionArea = self.initWeightSelectionArea(self.root)
		weightSelectionArea.pack(ipady = 3)

		fileSelectionArea = self.initFileSelectionArea(self.root)
		fileSelectionArea.pack(ipady = 3)

		complete = Button(self, text="Enter Flight Mode", command = self.finish)
		complete.pack(ipady = 5)  


	def initColorSelectionArea(self, master):
		colorSelectionArea = Frame(master)

		linesSelect = self.createColorSelectFrame(colorSelectionArea, "flightlines color", self.colour_flightlines, self.changeLinesColor)
		linesColorSelect = linesSelect[0]
		self.displayColorFlightlines = linesSelect[1]
		
		rampsSelect = self.createColorSelectFrame(colorSelectionArea, "ramps color", self.colour_ramps, self.changeRampsColor)
		rampsColorSelect = rampsSelect[0]
		self.displayColorRamps = rampsSelect[1]

		breadcrumbsSelect = self.createColorSelectFrame(colorSelectionArea, "breadcrumbs color", self.colour_breadcrumbs, self.changeBreadcrumbsColor)
		breadcrumbsColorSelect = breadcrumbsSelect[0]
		self.displayColorBreadcrumbs = breadcrumbsSelect[1]
		
		backgroundSelect = self.createColorSelectFrame(colorSelectionArea, "background color", self.colour_background, self.changeBackgroundColor)
		backgroundColorSelect = backgroundSelect[0]
		self.displayColorBackground = backgroundSelect[1]

		label = Label(colorSelectionArea, text="Choose Display Colors")

		label.pack(side=TOP, ipady=5)

		linesColorSelect.pack()#side=LEFT)
		rampsColorSelect.pack()#side=LEFT)
		breadcrumbsColorSelect.pack()#side=LEFT)
		backgroundColorSelect.pack()#side=LEFT)

		return colorSelectionArea

	def createColorSelectFrame(self, master, displayText, startingColor, buttonCallback):
		colorSelect = Frame(master)

		button = Button(colorSelect, text=displayText, command=buttonCallback)
		canvas = Canvas(colorSelect, background=startingColor, width=50, height=20) 

		canvas.pack(side=LEFT)
		button.pack(side=LEFT)


		return (colorSelect, canvas)

	def initWeightSelectionArea(self, master):
		weightSelectionArea = Frame(master) 

		flightlinesSelect = self.createWeightSelectFrame(weightSelectionArea, "Flightlines Weight", self.weight_flightplan) 
		flightlinesWeightSelect = flightlinesSelect[0]
		self.displayWeightFlightlines = flightlinesSelect[1]

		breadcrumbsSelect = self.createWeightSelectFrame(weightSelectionArea, "Breadcrumbs Weight", self.weight_breadcrumbs)  
		breadcrumbsWeightSelect = breadcrumbsSelect[0]
		self.displayWeightBreadcrumbs = breadcrumbsSelect[1]

		label = Label(weightSelectionArea, text="Choose Display Weights")

		label.pack(side=TOP, ipady=5)

		flightlinesWeightSelect.pack()#side=LEFT)
		breadcrumbsWeightSelect.pack()#side=LEFT) 

		return weightSelectionArea

	def createWeightSelectFrame(self, master, displayText, startingWeight):
		weightSelect = Frame(master)

		#button = Button(weightSelect, text=displayText, command=buttonCallback)
		#canvas = Canvas(weightSelect, background=startingColor, width=50, height=20) 

		#canvas.pack(side=LEFT)
		#button.pack(side=LEFT)

		label = Label(weightSelect, text=displayText)
		entry = Entry(weightSelect)
		entry.insert(INSERT, str(startingWeight)) 

		label.pack(side=LEFT)
		entry.pack(side=LEFT)

		return (weightSelect, entry)


	def initFileSelectionArea(self, master):
		FileSelectionArea = Frame(master) 

		flightlinesSelect = self.createFileSelectFrame(FileSelectionArea, "Flightlines File", self.chooseFlightlinesFile) 
		flightlinesFileSelect = flightlinesSelect[0]
		self.displayFileFlightlines = flightlinesSelect[1]

		flightrampsSelect = self.createFileSelectFrame(FileSelectionArea, "Flightramps File", self.chooseFlightrampsFile) 
		flightrampsFileSelect = flightrampsSelect[0]
		self.displayFileFlightramps = flightrampsSelect[1] 

		label = Label(FileSelectionArea, text="Choose Flight Plan Files") 

		label.pack(side=TOP, ipady=5)

		flightlinesFileSelect.pack()#side=LEFT)
		flightrampsFileSelect.pack()#side=LEFT) 

		return FileSelectionArea

	def createFileSelectFrame(self, master, displayText, callback):
		FileSelect = Frame(master)

		#button = Button(FileSelect, text=displayText, command=buttonCallback)
		#canvas = Canvas(FileSelect, background=startingColor, width=50, height=20) 

		#canvas.pack(side=LEFT)
		#button.pack(side=LEFT)

		button = Button(FileSelect, text=displayText, command=callback)
		entry = Entry(FileSelect) 

		entry.pack(side=LEFT)
		button.pack(side=LEFT)

		return (FileSelect, entry)


	def changeRampsColor(self):
		color = askcolor(self.colour_ramps)
		self.colour_ramps = color[1]
		self.displayColorRamps.config(background = color[1])

	def changeLinesColor(self):
		color = askcolor(self.colour_flightlines)
		self.colour_flightlines = color[1]
		self.displayColorFlightlines.config(background = color[1])

	def changeBackgroundColor(self):
		color = askcolor(self.colour_background)
		self.colour_background = color[1]
		self.displayColorBackground.config(background = color[1])

	def changeBreadcrumbsColor(self):
		color = askcolor(self.colour_breadcrumbs)
		self.colour_breadcrumbs = color[1]
		self.displayColorBreadcrumbs.config(background = color[1])

	def getFlightlinesWeight(self):
		return int(self.displayWeightFlightlines.get())

	def getBreadcrumbsWeight(self):
		return int(self.displayWeightBreadcrumbs.get()) 

	def chooseFlightlinesFile(self):
		path = tkFileDialog.askopenfilename()
		self.filepath_flightlines = path
		self.displayFileFlightlines.insert(INSERT, path)

	def chooseFlightrampsFile(self):
		path = tkFileDialog.askopenfilename()
		self.filepath_ramps = path 
		self.displayFileFlightramps.insert(INSERT, path)

	def getFlightlinesFile(self):
		return self.displayFileFlightlines.get()    

	def getFlightrampsFile(self):
		return self.displayFileFlightramps.get()    

	def getColors(self):
		return (self.colour_flightlines, self.colour_ramps, self.colour_breadcrumbs, self.colour_breadcrumbs)

	def getColorFlightlines(self):
		return self.colour_flightlines

	def getColorRamps(self):
		return self.colour_ramps

	def getColorBreadcrumbs(self):
		return self.colour_breadcrumbs

	def getColorBackground(self):
		return self.colour_background

	def finish(self):
		self.listening.leavePreFlightMode()

	def remove(self):
		for item in self.winfo_children():
   	 		item.pack_forget()
   	 		item.destroy() 

		self.pack_forget()
		self.destroy()

if __name__ == "__main__":
    # Starts the program.
    preflightMode = PreFlightMode(None, None) 
    preflightMode.mainloop()
    #preflightMode.run()