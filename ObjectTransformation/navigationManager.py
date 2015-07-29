import Tkinter as tk 		# for painting
from Tkinter import *		# for painting

from flightPlan import *	# flightplan - flightlines & ramps
from breadcrumbs import *	# breadcrumbs & plane

from time import sleep


class NavigationManager(Frame):
	"""
	The screen the pilot uses as they are flying the plane.
	This contains the display with the flightplan and breadcrumbs.
	This also contains buttons for the pilot to alter the display in-flight.

	@author: Kim Faughnan, Elizabeth Fong, Spring 2015
	"""

	# CONSTANT - time between calling refresh display
	refreshTime = 100

	# CONSTANT - zoon factors
	zoomInFactor = 1.1
	zoomOutFactor = 0.9

	# colour variables 
	colour_background = None
	colour_breadcrumbs = None
	colour_flightlines = None
	colour_ramps = None
	colour_plane = None

	# weight variables
	weight_breadcrumbs = None
	weight_flightplan = None

	# shapefile paths
	rampsFileName = None
	linesFileName = None

	# canvas
	canvas = None
	canvas_width = None
	canvas_height = None 

	# flight plan, breadcrumbs
	flightPlan = None 
	breadcrumbs = None

	# GPS Reader
	gpsReader = None 

	# scale, rotation (in radians, wrt North)
	scale = 1
	rotation = 0

	# coordinates for center - geographic & canvas coordinates
	centerLatLong = None 	# (latitude, longitude)
	centerXY = None
	
	# ground speed (from GPS)
	groundSpeed = 0

	# for smooth rotation
	rotationRefresh = 10
	smoothRotate = False
	rotateDelay = 10
	rotateIncrement = None


	# --- Construction -------------------------------------------- #

	def __init__(self, master, canvas_width, canvas_height, linesFileName, rampsFileName, colour_flightlines, colour_ramps, colour_breadcrumbs, colour_plane, colour_background, weight_flightplan, weight_breadcrumbs):
		"""
		Constructor: Initialises Navigation Manager. This is the screen the pilot uses in-flight.

		@param canvas_width: Width of the canvas.
		@param canvas_height: Height of the canvas.

		@param linesFileName: The path of the shapefile for the flightlines.
		@param rampsFileName: The path of the shapefile for the ramps.

		@param colour_flightlines: Colour of the flightlines.
		@param colour_ramps: Colour of the ramps.
		@param colour_breadcrumbs: Colour of the breadcrumbs.
		@param colour_plane: Colour for the representation of the plane.
		@param colour_background: Background colour.

		@param weight_flightplan: Line weight for the flight plan.
		@param weight_breadcrumbs: Point weight for the breadcrumbs.

		@return: None.
		"""
		Frame.__init__(self, master)

		# values from parameters
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
 		
		self.linesFileName = linesFileName
		self.rampsFileName = rampsFileName

		self.colour_flightlines = colour_flightlines
		self.colour_ramps = colour_ramps
		self.colour_breadcrumbs = colour_breadcrumbs
		self.colour_background = colour_background
		self.colour_plane = colour_plane

		self.weight_flightplan = weight_flightplan
		self.weight_breadcrumbs = weight_breadcrumbs
		
		# init window
		self.initWindow()
		
		# init flight plan
		self.flightPlan = FlightPlan(self.linesFileName, self.rampsFileName, self.colour_flightlines, self.colour_ramps, self.weight_flightplan, self.canvas)
		
		# initial scale, center geographic pt from flight plan
		self.scale = self.flightPlan.calculateInitialScale(self.canvas_width, self.canvas_height)
		self.centerLatLong = self.flightPlan.getInitialTranslation()  # we want to quickly overwrite this with a point from the gps
		
		print("\nstarting center lat long: {0}".format(self.centerLatLong))
		print("starting scale: {0}".format(self.scale)) 
		
		# canvas width & height, center x,y
		# needs to be after canvas added to screen (in initWindow)
		canvasWidth = self.canvas.winfo_width()
		canvasHeight = self.canvas.winfo_height()
		print("  canvas width: {0}\n  canvas height: {1}".format(canvasWidth, canvasHeight))
		self.centerXY = (canvasWidth/2, canvasHeight/2) 

		# init breadcrumbs
		self.breadcrumbs = Breadcrumbs(self.colour_breadcrumbs, self.weight_breadcrumbs, self.colour_plane) 
		
		# paint display
		self.refreshDisplay()


	def initWindow(self):
		"""
		Initialises the window with the user interface.

		@return: None.
		"""
		self.canvas = Canvas( self , width = self.canvas_width , height = self.canvas_height, background = self.colour_background )

		# buttons & text display
		buttons = Frame(self)
		zoomInButton = Button( buttons, text="+", command=self.zoomIn ) 
		zoomOutButton = Button( buttons, text="-", command=self.zoomOut )  
		clearButton = Button( buttons, text="clear", command=self.clearBreadcrumbs )  

		#textGroundSpeed = Text( self ) 
		#textGroundSpeed.insert(INSERT,"Ground Speed")

		# layout - packing
		self.canvas.pack(expand=True)
		zoomOutButton.pack(side=LEFT)
		zoomInButton.pack(side=LEFT)
		clearButton.pack(side=LEFT)
		
		buttons.pack(fill=tk.BOTH)
		#textGroundSpeed.grid()


	# --- On run -------------------------------------------------- #

	def run( self ) :
		"""
		On run. Refreshes the display after a pre-determined time (in milliseconds).

		@return: None.
		"""
		print("\n\nin run")

		self.refreshDisplay() 
		self.after( self.refreshTime , self.run ) 


	def refreshDisplay(self):
		"""
		Refreshes the display.

		@return: None.
		"""
		print("in refresh display")

		# clears canvas before painting
		self.canvas.delete("all")

		# get center canvas coordinate in case it changed
		canvasWidth = self.canvas.winfo_width()
		canvasHeight = self.canvas.winfo_height()
		self.centerXY = (canvasWidth/2, canvasHeight/2) 

		# paints display (flight plan, breadcrumbs)
		if self.smoothRotate:

			for i in range( 0 , self.rotationRefresh ):
				self.rotation += self.rotateIncrement
				self.flightPlan.paint( self.canvas, self.scale, self.rotation, self.centerLatLong, self.centerXY )
				self.breadcrumbs.paint( self.canvas, self.scale, self.rotation, self.centerLatLong, self.centerXY ) 
				sleep( self.rotateDelay )

			self.smoothRotate = False

		else:
			self.flightPlan.paint( self.canvas, self.scale, self.rotation, self.centerLatLong, self.centerXY )
			self.breadcrumbs.paint( self.canvas, self.scale, self.rotation, self.centerLatLong, self.centerXY ) 


	def newGPSData(self):
		"""
		Gets and processes new data from the GPS.
		This gets the geographic latitude and longitude, bearing, and ground speed from the GPS.

		@return: None.
		"""
		# add new geographic point from GPS to breadcrumbs
		self.centerLatLong = self.gpsReader.getLongLat()
		self.breadcrumbs.addPoint(self.centerLatLong)
		
		print("\n^^^^^^^^^^^^^^^^^^^^^^^^^\n   new point: {0}".format(self.centerLatLong))
		
		# get bearing & ground speed from GPS
		groundSpeedBearing = self.gpsReader.getGroundSpeedAndBearing()
		self.groundSpeed = groundSpeedBearing[0]

		# auto-rotate: need to be smooth
		newRotation = groundSpeedBearing[1]

		if newRotation != self.rotation:
			self.smoothRotate = True
			self.rotateIncrement = (newRotation - self.rotation) / self.rotationRefresh
		else:
			self.smoothRotate = False
			self.rotation = newRotation


	# --- Event Handling ------------------------------------------ #
	     
	def clearBreadcrumbs(self):
		"""
		Clears all added breadcrumbs from the display. 
		Does not remove them from memory.

		@return: None.
		"""
		self.breadcrumbs.clear()


	def zoomIn(self):
		"""
		Zooms into the display by a pre-determined amount.

		@return: None.
		"""
		self.zoom( self.zoomInFactor )


	def zoomOut(self):
		"""
		Zooms out of the display by a pre-determined amount.

		@return: None.
		"""
		self.zoom( self.zoomOutFactor )


	def zoom(self, factor):
		"""
		Zooms the display by the given factor.
		This multiplies the scale of the display by the given factor.

		@return: None.
		"""
		self.scale *= factor
		print("...\n  new scale: {0}\n...".format(self.scale))
		self.refreshDisplay()



# ----------------------------------------------------------------- #
# --- MAIN - FOR TESTING ------------------------------------------ #
# ----------------------------------------------------------------- #

if __name__ == "__main__":
    # Starts the program.
    navigationManager = NavigationManager() 
    navigationManager.mainloop()
    navigationManager.run()
