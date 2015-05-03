from point import Point		# for breadcrumbs
from line import Line		# representation of the plane


class Breadcrumbs() : 
	"""
	Breadcrumbs: The path that the plane has flown over.

	@author: Kim Faughnan, Elizabeth Fong, Spring 2015
	"""

	# Path: list of GPS coordinates of the plane
	path = None

	# breadcrumb point drawing variables
	pointSize = 5
	pointColor = "#135e1c" 

	# plane drawing variables
	planeSize = 6		# magnitude of dist from center pt to front tip pt
	planeColour = "#000000"
	planeWeight = 3 

	# breadcrumb drawing frequency - once every n points read from GPS
	drawingFreq = 3


	# --- Construction -------------------------------------------- #

	def __init__( self, pointColor, pointSize, planeColor ) :
		"""
		Constructor: Initialises the breadcrumbs for this flight.

		@param pointColor: The colour of the breadcrumbs.
		@param pointSize: The size of the breadcrumbs.
		@param planeColor: The colour of the plane.

		@return: None.
		"""
		self.path = [] 

		self.pointColor = pointColor
		self.pointSize = pointSize 
		self.planeColor = planeColor


	# --- Update Methods ------------------------------------------ #

	def addPoint( self , point ) :
		"""
		Adds the given point to the breadcrumbs.

		@param point: The most-recent breadcrumb.
		@return: None.
		"""
		adding = Point(point, self.pointColor, self.pointSize)
		self.path.append( adding )

		# sets this point to draw if this point matches the drawing frequency
		if len(self.path) % self.drawingFreq != 0 :
			adding.setPaint( False )


	def clear( self ) :
		"""
		Clears all the breadcrumbs from the display.
		This only sets the painting of each point to false, 
		but does not remove them from the list.

		@return: None.
		"""
		for point in self.path:
			point.setPaint( False )


	# --- Painting ------------------------------------------------ #

	def paint( self , canvas , scale , rotation , centerLatLong , centerXY ) :
		"""
		Paints the breadcrumbs and the plane onto the canvas.
		This draws every n points, determined by the painting frequency,
		starting from the most recently added.

		@param canvas: The canvas the breadcrumbs and plane are to be drawn onto.
		@param scale: Magnitude of the scale required to convert geographic coordinates to canvas coordinates.
					  Used for calculating the canvas coordinates of the breadcrumbs before painting.
		@param rotation: The angle, in radians, from North that the points and the plane are to be rotated by, 
						 in a clockwise direction, relative to the center point.
						 Used for calculating the canvas coordintates of the breadcrumbs and the plane before painting.
		@param centerLatLong: Geographic latitude, longitude of the center point.
							  Used for calculating the canvas coordinates of the breadcrumbs before painting.
							  Represented as a duple.
		@param centerXY: Canvas x and y-coordinates of the center point.
						 Used for calculating the canvas coordintates of the breadcrumbs and the plane before painting.
						 Represented as a duple.

		@return: None.
		"""
		# painting breadcrumbs
		print("	painting breadcrumbs")
		
		for point in reversed(self.path):
			point.paint(canvas , scale , rotation , centerLatLong , centerXY )  

		# painting plane
		adjustedCenter = ( centerXY[0] - self.pointSize/2 , centerXY[1] - self.pointSize/2 )
		self.drawPlane( canvas , rotation , adjustedCenter )


	def drawPlane( self , canvas , rotation , centerXY ) :
		"""
		Draws the plane onto the canvas. 
		The plane is represented by an isosceles triangle,
		with its tip facing the direction given by the GPS.

		@param canvas: The canvas the plane is to be drawn on.
		@param rotation: The angle, in radians, from North this plane is facing. Given by the GPS.
		@param centerXY: Canvas x and y-coordinates for the center point.

		@return: None.
		"""
		# plane: a set of 3 lines
		# draw as if rotation is 0 , then rotate before painting
		centerX = centerXY[0]
		centerY = centerXY[1]

		tip = ( centerX , centerY-self.planeSize )
		left = ( centerX-self.planeSize , centerY+self.planeSize )
		right = ( centerX+self.planeSize , centerY+self.planeSize )

		line1 = Line( tip , left , self.planeColour , self.planeWeight )
		line2 = Line( tip , right , self.planeColour , self.planeWeight )
		line3 = Line( left , right , self.planeColour , self.planeWeight )

		line1.paintPlaneLine( canvas , rotation , centerXY )
		line2.paintPlaneLine( canvas , rotation , centerXY )
		line3.paintPlaneLine( canvas , rotation , centerXY )
