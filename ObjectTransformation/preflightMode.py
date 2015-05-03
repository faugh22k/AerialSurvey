# Imports - User Interface
import Tkinter as tk
from Tkinter import *
import ttk
from tkColorChooser import askcolor
import tkFileDialog


class PreFlightMode(Frame) :
	"""
	Pre-flight Mode.

	@author: Kim Faughnan, Elizabeth Fong, Spring 2015.
	"""
	
	# colour variables - default
	colour_background = "#3b98e3"
	colour_breadcrumbs = "#135e1c"
	colour_flightlines = "#ffff33"
	colour_ramps = "#ff0000"
	colour_plane = "#000000"

	# colour selection widgets
	colorSelectionAreaWidgets = []

	# display selection variables
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

	# file selector filters
	fileTypeOptions = [("Flightplan Files", "*.shp")]

	# file selector to get paths of files
	# user selects both flightlines file and ramps file
	filepath_flightlines = None
	filepath_ramps = None

	# event listener
	listening = None

	# root - frame of the program
	root = None


	# --- Construction -------------------------------------------- #

	def __init__( self, master, listening ) :
		"""
		Constructor: Initialises the pre-flight mode display.

		@param master: The frame of the window for this program.
		@param listening: The event listener

		@return: None.
		"""
		Frame.__init__(self, master)
		
		if (master is None): 
			master = self
		self.root = master
		
		self.listening = listening
		self.initWindow()


	def initWindow(self):
		"""
		Initialises the window with user selection options.
		Options: Colour, Line/Point weight, file paths for flightlines and ramps.

		@return: None.
		"""
		# colour selection
		colorSelectionArea = self.initColorSelectionArea(self.root)
		colorSelectionArea.pack(ipady = 3, fill=tk.BOTH)

		# line/point weight selection
		weightSelectionArea = self.initWeightSelectionArea(self.root)
		weightSelectionArea.pack(ipady = 3)

		# file selector
		fileSelectionArea = self.initFileSelectionArea(self.root)
		fileSelectionArea.pack(ipady = 3)  


	# --- Colour Selector - part of construction ------------------ #

	def initColorSelectionArea(self, master):
		"""
		Creates and returns the colour selection area.

		@param master: The root of this area.
		@return: The colour selection area.
		"""
		colorSelectionArea = Frame(master, background = self.colour_background) 

		# flightlines
		linesSelect = self.createColorSelectFrame(colorSelectionArea, "flightlines color", self.colour_flightlines, self.changeLinesColor)
		linesColorSelect = linesSelect[0]
		self.displayColorFlightlines = linesSelect[1]
		
		# ramps
		rampsSelect = self.createColorSelectFrame(colorSelectionArea, "ramps color", self.colour_ramps, self.changeRampsColor)
		rampsColorSelect = rampsSelect[0]
		self.displayColorRamps = rampsSelect[1]

		# breadcrumbs
		breadcrumbsSelect = self.createColorSelectFrame(colorSelectionArea, "breadcrumbs color", self.colour_breadcrumbs, self.changeBreadcrumbsColor)
		breadcrumbsColorSelect = breadcrumbsSelect[0]
		self.displayColorBreadcrumbs = breadcrumbsSelect[1]

		# plane
		planeSelect = self.createColorSelectFrame(colorSelectionArea, "plane location color", self.colour_plane, self.changePlaneColor)
		planeColorSelect = planeSelect[0]
		self.displayColorPlane = planeSelect[1]
		
		# background
		backgroundSelect = self.createColorSelectFrame(colorSelectionArea, "background color", self.colour_background, self.changeBackgroundColor)
		backgroundColorSelect = backgroundSelect[0]
		self.displayColorBackground = backgroundSelect[1]

		# display label for this area
		label = Label(colorSelectionArea, text="Choose Display Colors")
		label.pack(side=TOP, ipady=5, fill=tk.BOTH)

		# packing display components
		linesColorSelect.pack()
		rampsColorSelect.pack()
		breadcrumbsColorSelect.pack()
		planeColorSelect.pack()
		backgroundColorSelect.pack()

		# colour selection widgets - preview colour in the display after selection.
		self.colorSelectionAreaWidgets = [colorSelectionArea, label]

		for item in self.colorSelectionAreaWidgets:
			print(item)
			if isinstance(item, tuple):
				for widget in item:
					widget.config(background = self.colour_background)
			else:
				item.config(background = self.colour_background)

		return colorSelectionArea


	def createColorSelectFrame(self, master, displayText, startingColor, buttonCallback):
		"""
		Creates a frame for a colour selection area.

		@param master: The root of this frame.
		@param displayText: The display text for this frame.
		@param startingColor: The initial background colour of this frame.
		@param buttonCallback: The method to be called when the button is clicked.

		@return The frame for the colour selection area.
		"""
		colorSelect = Frame(master)

		button = Button(colorSelect, text=displayText, command=buttonCallback)
		canvas = Canvas(colorSelect, background=startingColor, width=50, height=20) 

		canvas.pack(side=LEFT)
		button.pack(side=LEFT)

		return (colorSelect, canvas)


	# --- Weight Selector - part of construction ------------------ #

	def initWeightSelectionArea(self, master):
		"""
		Creates and returns the line/point weight selection area.

		@param master: The root of this area.
		@return: The line/point weight selection area.
		"""
		weightSelectionArea = Frame(master) 

		# flightlines
		flightlinesSelect = self.createWeightSelectFrame(weightSelectionArea, "Flightlines Weight", self.weight_flightplan) 
		flightlinesWeightSelect = flightlinesSelect[0]
		self.displayWeightFlightlines = flightlinesSelect[1]

		# breadcrumbs
		breadcrumbsSelect = self.createWeightSelectFrame(weightSelectionArea, "Breadcrumbs Weight", self.weight_breadcrumbs)  
		breadcrumbsWeightSelect = breadcrumbsSelect[0]
		self.displayWeightBreadcrumbs = breadcrumbsSelect[1]

		# display label
		label = Label(weightSelectionArea, text="Choose Display Weights")

		# pack components
		label.pack(side=TOP, ipady=5)

		flightlinesWeightSelect.pack()
		breadcrumbsWeightSelect.pack() 

		return weightSelectionArea


	def createWeightSelectFrame(self, master, displayText, startingWeight):
		"""
		Creates a frame for a weight selection area.

		@param master: The root of this frame.
		@param displayText: The display text for this frame.
		@param startingWeight: The default weight.

		@return: The frame for the weight selection area.
		"""
		weightSelect = Frame(master)

		# create label and entry
		label = Label(weightSelect, text=displayText)
		entry = Entry(weightSelect)
		entry.insert(INSERT, str(startingWeight)) 

		# pack components
		label.pack(side=LEFT)
		entry.pack(side=LEFT)

		return (weightSelect, entry)


	# --- File Selector - part of construction -------------------- #

	def initFileSelectionArea(self, master):
		"""
		Creates and returns the file selection area.

		@param master: The root of this area.
		@return: The file selection area.
		"""
		FileSelectionArea = Frame(master) 

		# flightlines
		flightlinesSelect = self.createFileSelectFrame(FileSelectionArea, "Flightlines File", self.chooseFlightlinesFile) 
		flightlinesFileSelect = flightlinesSelect[0]
		self.displayFileFlightlines = flightlinesSelect[1]

		# ramps
		flightrampsSelect = self.createFileSelectFrame(FileSelectionArea, "Flightramps File", self.chooseFlightrampsFile) 
		flightrampsFileSelect = flightrampsSelect[0]
		self.displayFileFlightramps = flightrampsSelect[1] 

		# display label
		label = Label(FileSelectionArea, text="Choose Flight Plan Files") 

		# pack components
		label.pack(side=TOP, ipady=5)

		flightlinesFileSelect.pack()
		flightrampsFileSelect.pack()

		return FileSelectionArea


	def createFileSelectFrame(self, master, displayText, callback):
		"""
		Creates a frame for a file selection area.

		@param master: The root of this frame.
		@param displayText: The display text for this frame.
		@param callback: The handler to be called when the button is clicked.

		@return: The frame for the file selection area.
		"""
		FileSelect = Frame(master)

		# create components
		button = Button(FileSelect, text=displayText, command=callback)
		entry = Entry(FileSelect) 

		# pack components
		entry.pack(side=LEFT)
		button.pack(side=LEFT)

		return (FileSelect, entry)


	# --- Event Handlers - Colour --------------------------------- #

	def changeRampsColor(self):
		"""
		Event Handler - Changes the colour for ramps to the selected colour.

		@return: None.
		"""
		color = askcolor(self.colour_ramps)

		if color[1] is None:
			return

		self.colour_ramps = color[1]
		self.displayColorRamps.config(background = color[1])


	def changeLinesColor(self):
		"""
		Event Handler - Changes the colour for flightlines to the selected colour.
		
		@return: None.
		"""
		color = askcolor(self.colour_flightlines) 

		if color[1] is None:
			return

		self.colour_flightlines = color[1]
		self.displayColorFlightlines.config(background = color[1])


	def changeBackgroundColor(self):
		"""
		Event Handler - Changes the background colour to the selected colour.
		
		@return: None.
		"""
		color = askcolor(self.colour_background) 

		if color[1] is None:
			return

		self.colour_background = color[1]
		self.displayColorBackground.config(background = color[1])

		# changes the background for the widget as well
		for widget in self.colorSelectionAreaWidgets:
			print("updating backrounds")
			widget.config(background = color[1]) 


	def changeBreadcrumbsColor(self):
		"""
		Event Handler - Changes the colour for breadcrumbs to the selected colour.
		
		@return: None.
		"""
		color = askcolor(self.colour_breadcrumbs)  

		if color[1] is None:
			return

		self.colour_breadcrumbs = color[1]
		self.displayColorBreadcrumbs.config(background = color[1])


	def changePlaneColor(self):
		"""
		Event Handler - Changes the colour for the plane to the selected colour.
		
		@return: None.
		"""
		color = askcolor(self.colour_plane) 

		if color[1] is None:
			return

		self.colour_plane = color[1]
		self.displayColorPlane.config(background = color[1])


	# --- Event Handlers - File Choosers -------------------------- #

	def chooseFlightlinesFile(self):
		"""
		Event Handler - Changes the path to the flightlines shapefile to the selected path.
		
		@return: None.
		"""
		path = tkFileDialog.askopenfilename(filetypes = self.fileTypeOptions)

		self.filepath_flightlines = path
		self.displayFileFlightlines.insert(INSERT, path)


	def chooseFlightrampsFile(self):
		"""
		Event Handler - Changes the path to the ramps shapefile to the selected path.
		
		@return: None.
		"""
		path = tkFileDialog.askopenfilename(filetypes = self.fileTypeOptions)

		self.filepath_ramps = path 
		self.displayFileFlightramps.insert(INSERT, path)


	# --- Getters - Colour ---------------------------------------- #

	def getColors(self):
		"""
		Returns the selected component colours as a tuple, with the format
		(flightlines, ramps, breadcrumbs, background, plane)

		@return: The selected component colours.
		"""
		return (self.colour_flightlines, self.colour_ramps, self.colour_breadcrumbs, self.colour_background, self.colour_plane)


	def getColorFlightlines(self):
		"""
		Returns the selected colour of the flightlines.
		@return: The selected colour of the flightlines.
		"""
		return self.colour_flightlines


	def getColorRamps(self):
		"""
		Returns the selected colour of the ramps.
		@return: The selected colour of the ramps.
		"""
		return self.colour_ramps


	def getColorBreadcrumbs(self):
		"""
		Returns the selected colour of the breadcrumbs.
		@return: The slected colour of the breadcrumbs.
		"""
		return self.colour_breadcrumbs


	def getColorBackground(self):
		"""
		Returns the selected background colour.
		@return: The selected background colour.
		"""
		return self.colour_background


	def getColorPlane( self ) :
		"""
		Returns the selected colour of the plane.
		@return: The selected colour of the plane.
		"""
		return self.colour_plane


	# --- Getters - Line/Point Weights ---------------------------- #

	def getFlightlinesWeight(self):
		"""
		Returns the selected line weight for the flightlines.
		@return: The selected line weight for the flightlines.
		"""
		return int(self.displayWeightFlightlines.get())


	def getBreadcrumbsWeight(self):
		"""
		Returns the selected point weight for the breadcrumbs.
		@return: The selected point weight for the breadcrumbs.
		"""
		return int(self.displayWeightBreadcrumbs.get()) 


	# --- Getters - File Paths ------------------------------------ #

	def getFlightlinesFile(self):
		"""
		Returns the file path to the selected flightlines shapefile.
		@return: The file path to the selected flightlines shapefile.
		"""
		return self.displayFileFlightlines.get()    


	def getFlightrampsFile(self):
		"""
		Returns the file path to the selected ramps shapefile.
		@return: The file path to the selected ramps shapefile.
		"""
		return self.displayFileFlightramps.get()    


	# --- Exit Pre-flight Mode ------------------------------------ #

	def finish(self):
		"""
		Event listener - Leaves pre-flight mode.
		@return: None.
		"""
		self.listening.leavePreFlightMode()


	def remove(self):
		"""
		Removes this screen from the window.
		@return: None.
		"""
		# remove components
		for item in self.winfo_children():
   	 		item.pack_forget()
   	 		item.destroy() 

   	 	# remove self
		self.pack_forget()
		self.destroy()



# ----------------------------------------------------------------- #
# --- MAIN - FOR TESTING ------------------------------------------ #
# ----------------------------------------------------------------- #

if __name__ == "__main__":
    # Starts the program.
    preflightMode = PreFlightMode(None, None) 
    preflightMode.mainloop()
    #preflightMode.run()
