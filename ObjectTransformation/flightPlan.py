
import shapefile  		# for reading in shapefiles
from line import * 		# represents flightlines, ramps


class FlightPlan() :
	"""
	The flightplan. This contains flightlines and ramps.

	@author: Kim Faughnan, Elizabeth Fong, Spring 2015
	"""
	# flightlines, ramps
	lines = None
	ramps = None

	# the canvas for drawing on
	canvas = None

	# colour variables
	lineColor = None
	rampColor = None
	
	# line width for the flight plan
	drawingWidth = None

	# size of this flight plan
	width = None
	height = None

	# min geographic coordinate of this flight plan
	minX = None
	minY = None


	# --- Construction -------------------------------------------- #

	def __init__(self, fileNameLines, fileNameRamps, lineColor, rampColor, drawingWidth, canvas): 
		"""
		Constructor:
		Initialises the flight plan object by reading in the flightlines 
		and ramps files and creating Line objects for them.

		@param fileNameLines: The path for the shapefile of the flightlines.
		@param fileNameRamps: The path for the shapefile of the ramps.
		@param lineColor: The colour of the flightlines.
		@param rampColor: The colour of the ramps.
		@param drawingWidth: The line width for the flightlines and ramps.
		@param canvas: The canvas the flight plan is to be drawn on.

		@return: None.
		"""
		lines = shapefile.Reader(fileNameLines)
		ramps = shapefile.Reader(fileNameRamps)

		self.canvas = canvas

		self.lineColor = lineColor
		self.rampColor = rampColor
		self.drawingWidth = drawingWidth

		self.lines = []
		self.ramps = [] 

		# init flightlines, ramps
		for shape in lines.shapes(): 
			points = shape.points
			self.lines.append(Line((points[0][0] , points[0][1]) , (points[1][0] , points[1][1]), self.lineColor, self.drawingWidth))  
		
		for shape in ramps.shapes(): 
			points = shape.points
			self.ramps.append(Line((points[0][0] , points[0][1]) , (points[1][0] , points[1][1]), self.rampColor, self.drawingWidth))  
		
		# calculate width & height of entire flightplan, enables calculating initial scale.
		self.getWidthHeight()


	# --- Calculations -------------------------------------------- #

	def getWidthHeight(self):
		"""
		Calculates and returns the width and height of this flight plan.

		@return: The width and height of this flight plan, as a duple, with the formath (width,height).
		"""
		minX = float("inf")  
		maxX = float("-inf")  
		minY = float("inf") 
		maxY = float("-inf") 

		print("     ^^^^^      ")

		# compare flightlines to get min x,y and max x,y
		for shape in self.lines:
			points = shape.getPoints()  

			for point in points:
				minX = min(point.x, minX)
				maxX = max(point.x, maxX)

				minY = min(point.y, minY)
				maxY = max(point.y, maxY)
				print("      point: {0}    {1}".format(point.x, point.y)) 

		# compare ramps to get min x,y and max x,y
		for shape in self.ramps:
			points = shape.getPoints()  

			for point in points:
				minX = min(point.x, minX)
				maxX = max(point.x, maxX)

				minY = min(point.y, minY)
				maxY = max(point.y, maxY)
				print("      point: {0}    {1}".format(point.x, point.y))

		# calculate width, height
		self.width = maxX - minX	
		self.height = maxY - minY

		self.minX = minX
		self.minY = minY 

		print("\nin getWidthHeight")
		print("   minX: {0}\n   maxX: {1}".format(minX, maxX))
		print("   minY: {0}\n   maxY: {1}".format(minY, maxY))
		print("   width: {0}\n   height: {1}".format(self.width, self.height))

		return (self.width, self.height)


	def calculateInitialScale(self, canvasWidth, canvasHeight):
		"""
		Calculates the initial scale for the canvas.
		This scale would enable the entire flight plan to be shown on the display.

		@param canvasWidth: The width of the canvas.
		@param canvasHeight: The height of the canvas.

		@return: The initial scale.
		"""
		widthRatio = canvasWidth/self.width
		heightRatio = canvasHeight/self.height

		print("\nin calculateInitialScale: ")
		print("   canvasWidth: {0}\n   canvasHeight: {1}\n   width: {2}\n   height: {3}".format(canvasWidth, canvasHeight, self.width, self.height))
		print("   widthRatio: {0}\n   heightRatio: {1}\n   chosenRatio: {2}".format(widthRatio, heightRatio, min(widthRatio,heightRatio)))
		
		return min(widthRatio, heightRatio) 


	def getInitialTranslation(self):
		"""
		Returns the initial translation, so that the minimum 
		x and y-coordinates will be displayed on the canvas.
		
		@return: The initial translation, as a duple, with the format (minX,minY).
		"""
		return (self.minX, self.minY)


	def getInitialCenter(self):
		"""
		Returns the initial center point.
		This is the coordinates of the center of the flight plan.

		@return: The inital center point, as a duple, with the format (x,y).
		"""
		return (self.minX + (self.width/2), self.minY + (self.height/2)) 

	
	# --- Painting ------------------------------------------------ #

	def paint(self, canvas , scale , rotation , centerLatLong , centerXY ):
		"""
		Paints the flight plan onto the canvas.

		@param canvas: The canvas this flight plan is to be drawn onto.
		@param scale: Magnitude of the scale required to convert geographic coordinates to canvas coordinates.
					  Used for calculating the canvas coordinates of this flight plan before painting.
		@param rotation: The angle, in radians, from North that this flight plan is to be rotated by, 
						 in a clockwise direction, relative to the center point.
						 Used for calculating the canvas coordintates of this flight plan before painting.
		@param centerLatLong: Geographic latitude, longitude of the center point.
							  Used for calculating the canvas coordinates of this flight plan before painting.
							  Represented as a duple.
		@param centerXY: Canvas x and y-coordinates of the center point.
						 Used for calculating the canvas coordintates of this flight plan before painting.
						 Represented as a duple.

		@return: None.
		"""
		for item in self.ramps: 
			item.paint(self.canvas , scale , rotation , centerLatLong , centerXY ) 

		for item in self.lines:
			item.paint(self.canvas , scale , rotation , centerLatLong , centerXY )
