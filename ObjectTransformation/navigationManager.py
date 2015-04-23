from Tkinter import *
#TMPgps*import gpsReader
from flightPlan import *
from breadcrumbs import *

class NavigationManager(Frame):

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

	# weight variables
	weight_breadcrumbs = None
	weight_flightplan = None

	currentScale = 1
	centerX = 0
	centerY = 0
	translateX = 0
	translateY = 0 
	rotation = 0
	groundSpeed = 0

	def __init__(self, master, canvas_width, canvas_height, linesFileName, rampsFileName, colour_flightlines, colour_ramps, colour_breadcrumbs, colour_background, weight_flightplan, weight_breadcrumbs):
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

		self.weight_flightplan = weight_flightplan
		self.weight_breadcrumbs = weight_breadcrumbs
		
		self.initWindow()
		
		self.flightPlan = FlightPlan(self.linesFileName, self.linesFileName, self.colour_flightlines, self.colour_ramps, self.weight_flightplan, self.canvas)
		
		self.currentScale = self.flightPlan.calculateInitialScale(self.canvas_width, self.canvas_height)
		translation = self.flightPlan.getInitialTranslation()
		self.centerX = translation[0]
		self.centerY = translation[1]

		self.breadcrumbs = Breadcrumbs(self.colour_breadcrumbs, self.weight_breadcrumbs) 
		#TMPgps*self.gpsReader = GPSReader()
		#TMPgps*self.gpsReader.initConnections() 


		# TMPdefaults*
		#self.currentScale = 1
		#self.translateX = 80
		#self.translateY = 80


		self.refreshDisplay()

	def initWindow(self):
		self.canvas = Canvas( self , width = self.canvas_width , height = self.canvas_height, background = self.colour_background )

		zoomInButton = Button( self, text="+", command=self.zoomIn ) 
		zoomOutButton = Button( self, text="-", command=self.zoomIn ) 

		#textGroundSpeed = Text( self ) 
		#textGroundSpeed.insert(INSERT,"Ground Speed")

		self.canvas.pack()
		zoomInButton.pack()
		zoomOutButton.pack()
		#textGroundSpeed.grid()


	def refreshDisplay(self):
		print("in refresh display")
		#self.translate() 
		#TMProtate*self.rotate()
		#self.scale()    

		#self.canvas.create_line( 0 , 0 , 500 , 500 , fill = "#ffff33" , width = 3 )

		#self.canvas.create_line( self.translateX , self.translateY , self.translateX+200 , self.translateY+200 , fill = "#ff0000" , width = 3 ) 

		self.flightPlan.paint(self.canvas)
		self.breadcrumbs.paint(self.canvas)

	def translate(self): 
		print("translating by {0}, {1}".format(self.translateX, self.translateY))
		self.breadcrumbs.translate(self.translateX, self.translateY)
		self.flightPlan.translate(self.translateX, self.translateY) 

	def scale(self): 
		print("scaling by {0}".format(self.currentScale))
		self.breadcrumbs.scale(self.currentScale, (self.centerX, self.centerY))
		self.flightPlan.scale(self.currentScale, (self.centerX, self.centerY))

	def rotate(self): 
		print("rotating by {0}".format(self.rotation))
		self.breadcrumbs.rotate(self.rotation)
		self.flightPlan.rotate(self.rotation) 

	def zoomIn(self):
		self.zoom(1.1)


	def zoomOut(self):
		self.zoom(0.9)

	def zoom(self, factor):
		self.currentScale *= factor

	def newGPSData(self):
		#TMPgps*longLat = self.gpsReader.getLongLat() 

		self.breadcrumbs.addPoint(longLat)
		self.centerX = longLat[1]
		self.centerY = longLat[0] 

		#TMPgps*self.rotation = self.gpsReader.getBearing()
		#TMPgps*self.groundSpeed = self.gpsReader.getGroundSpeed()

	def run(self):
		print("in run")
		#self.mainloop()

		#while True:
		#	#TMPgps*self.newGPSData()
		#
		#	self.refreshDisplay()







if __name__ == "__main__":
    # Starts the program.
    navigationManager = NavigationManager() 
    navigationManager.mainloop()
    navigationManager.run()






