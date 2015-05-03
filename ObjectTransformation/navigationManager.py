import Tkinter as tk 		# for painting
from Tkinter import *		# for painting

from flightPlan import *	# flightplan - flightlines & ramps
from breadcrumbs import *	# breadcrumbs & plane


class NavigationManager(Frame):
	"""
	The screen the pilot uses as they are flying the plane.
	This contains the display with the flightplan and breadcrumbs.
	This also contains buttons for the pilot to alter the display in-flight.

	@author: Kim Faughnan, Elizabeth Fong, Spring 2015
	"""

	flightPlan = None 
	breadcrumbs = None 
	gpsReader = None 

	rampsFileName = None
	linesFileName = None

	canvas = None
	canvas_width = None
	canvas_height = None 

	# colour variables 
	colour_background = None
	colour_breadcrumbs = None
	colour_flightlines = None
	colour_ramps = None
	colour_plane = None

	# weight variables
	weight_breadcrumbs = None
	weight_flightplan = None

	scale = 1
	centerXY = None
	centerLatLong = None # (latitude, longitude)
	rotation = 0
	groundSpeed = 0

	index = 0 # for temporary hardcoded breadcrumbs list

	def __init__(self, master, canvas_width, canvas_height, linesFileName, rampsFileName, colour_flightlines, colour_ramps, colour_breadcrumbs, colour_plane, colour_background, weight_flightplan, weight_breadcrumbs):
		Frame.__init__(self, master) # (self, master)
		#self.pack()

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
		
		self.initWindow()
		
		self.flightPlan = FlightPlan(self.linesFileName, self.rampsFileName, self.colour_flightlines, self.colour_ramps, self.weight_flightplan, self.canvas)
		
		self.scale = self.flightPlan.calculateInitialScale(self.canvas_width, self.canvas_height)
		self.centerLatLong = self.flightPlan.getInitialTranslation()  # we want to quickly overwrite this with a point from the gps
		
		print("\nstarting center lat long: {0}".format(self.centerLatLong))
		print("starting scale: {0}".format(self.scale)) 
		
		# needs to be after canvas added to screen (in initWindow)
		canvasWidth = self.canvas.winfo_width()
		canvasHeight = self.canvas.winfo_height()
		print("  canvas width: {0}\n  canvas height: {1}".format(canvasWidth, canvasHeight))
		self.centerXY = (canvasWidth/2, canvasHeight/2) 

		self.breadcrumbs = Breadcrumbs(self.colour_breadcrumbs, self.weight_breadcrumbs, self.colour_plane) 
		#**self.gpsReader = GPSReader()
		#**self.gpsReader.initConnections() 
		#self.breadcrumbs.addPoint(self.centerLatLong) # TMP hardcoded temporary TODO

		# TMPdefaults*
		#self.scale = 1
		#self.translateX = 80
		#self.translateY = 80


		self.refreshDisplay()

	def initWindow(self):
		self.canvas = Canvas( self , width = self.canvas_width , height = self.canvas_height, background = self.colour_background )

		buttons = Frame(self)
		#zoomInButton = Button( self, text="+", command=self.zoomIn )  
		#zoomOutButton = Button( self, text="-", command=self.zoomOut ) 
		zoomInButton = Button( buttons, text="+", command=self.zoomIn ) 
		zoomOutButton = Button( buttons, text="-", command=self.zoomOut )  
		clearButton = Button( buttons, text="clear", command=self.clearBreadcrumbs )  

		#textGroundSpeed = Text( self ) 
		#textGroundSpeed.insert(INSERT,"Ground Speed")

		#self.canvas.pack(fill=tk.X)
		self.canvas.pack(expand=True)
		zoomOutButton.pack(side=LEFT)
		zoomInButton.pack(side=LEFT)
		clearButton.pack(side=LEFT)
		
		buttons.pack(fill=tk.BOTH)
		#textGroundSpeed.grid()


	def refreshDisplay(self):
		print("in refresh display")  

		self.canvas.delete("all")

		canvasWidth = self.canvas.winfo_width()
		canvasHeight = self.canvas.winfo_height()
		#print("  canvas width: {0}\n  canvas height: {1}".format(canvasWidth, canvasHeight))
		self.centerXY = (canvasWidth/2, canvasHeight/2) 
		#print("  canvas center:  {0} \n ".format(self.centerXY)) 

		#self.canvas.create_line( 0 , 0 , 500 , 500 , fill = "#ffff33" , width = 3 )

		#self.canvas.create_line( self.translateX , self.translateY , self.translateX+200 , self.translateY+200 , fill = "#ff0000" , width = 3 ) 

		self.flightPlan.paint( self.canvas, self.scale, self.rotation, self.centerLatLong, self.centerXY )
		self.breadcrumbs.paint( self.canvas, self.scale, self.rotation, self.centerLatLong, self.centerXY ) 

		#testPoint = Point((-72.57663069977029, 35), "#59DE42", 6)
		#testPoint.paint( self.canvas, self.scale, self.rotation, self.centerLatLong, self.centerXY )

		#self.canvas.create_line( self.centerXY[0] , self.centerXY[1] , self.centerXY[0] , self.centerXY[1]+3 , fill = "#FF0066" , width = 3 )
	     
	def clearBreadcrumbs(self):
		self.breadcrumbs.clear()

	def zoomIn(self):
		self.zoom(1.1)


	def zoomOut(self):
		self.zoom(0.9)

	def zoom(self, factor):
		self.scale *= factor
		print("...\n  new scale: {0}\n...".format(self.scale))
		self.refreshDisplay()

	def newGPSData(self):
		#print ("  about to ask for new long lat")
		#line = raw_input()
		self.centerLatLong = self.gpsReader.getLongLat()
		#print ("  about to add new breadcrumb")
		#line = raw_input()   
		self.breadcrumbs.addPoint(self.centerLatLong)
		
		
		#breadcrumbsFake = [(-72.57398,42.25478),(-72.57387,42.254746),(-72.57380,42.254724),(-72.57369,42.254687),(-72.57362,42.254665),(-72.57356,42.254646),(-72.57345,42.254609),(-72.57338,42.254586),(-72.57326,42.254549),  (-72.57294,42.254445)]
		#if (self.index < len(breadcrumbsFake)):
		#self.centerLatLong = breadcrumbsFake[self.index]
		#self.index += 1 
		print("\n^^^^^^^^^^^^^^^^^^^^^^^^^\n   new point: {0}".format(self.centerLatLong))
		#self.breadcrumbs.addPoint(self.centerLatLong)
		
		#self.breadcrumbs.addPoint(self.centerLatLong)
		#self.rotation = self.gpsReader.getBearing()
		#self.groundSpeed = self.gpsReader.getGroundSpeed()
		groundSpeedBearing = self.gpsReader.getGroundSpeedAndBearing()

		self.rotation = groundSpeedBearing[1]
		self.groundSpeed = groundSpeedBearing[0]


	def run(self):
		print("\n\nin run")
		#index = 0
		#self.mainloop()

		# while True:
		# 	print("about to get new gps data")  
		# 	line = raw_input()
		# 	self.newGPSData() 

		# 	print ("about to update display")
		# 	line = raw_input()

		# 	self.refreshDisplay() 
		# 	#index += 1
		# 	#if index > 5:
		# 	#	return
		# 	print ("about to enter new update loop")
		# 	line = raw_input()

		#**self.newGPSData() 

		self.refreshDisplay() 

		self.after(100, self.run) 

		#self.refreshDisplay()







if __name__ == "__main__":
    # Starts the program.
    navigationManager = NavigationManager() 
    navigationManager.mainloop()
    navigationManager.run()





