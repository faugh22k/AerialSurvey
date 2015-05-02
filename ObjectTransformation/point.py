from Tkinter import *	# for drawing
import math				# for calculations


class Point() :
	"""
	A Point

	@author Elizabeth Fong, Kim Faughnan, Spring 2015
	"""
	# Painting variables
	colour = None
	weight = None

	# boolean variable to paint this point or not
	toPaint = None

	# Geographic latitude, longitude values of this point
	latitude = None
	longitude = None
	
	# Canvas coordinates: x,y (width,height) distances wrt to (0,0) of canvas
	x = None
	y = None


	# --- Construction -------------------------------------------- #

	def __init__( self , geoPt , ptColour , ptWeight ) :
		"""
		Constructor: Initialises this point.

		@param geoPt: Geographic latitude , longitude of this point. Represented as a duple.
		@param ptColour: The colour of this point. None if this point is part of a line.
		@param ptWeight: The weight of this point. None if this point is part of a line.

		@return: None.
		"""
		self.latitude = geoPt[0]
		self.longitude = geoPt[1]

		self.x = geoPt[0]
		self.y = geoPt[1]

		self.colour = ptColour
		self.weight = ptWeight
		self.toPaint = True


	# --- Transformation ------------------------------------------ #

	def calculateXY( self , scale , rotation , centerLatLong , centerXY ) :
		"""
		Calculates the canvas coordinates of this point.

		@param scale: Magnitude of the scale required to convert geographic coordinates to canvas coordinates.
		@param rotation: The angle, in radians, from North that this point is to be rotated by, in a clockwise direction, relative to the center point.
		@param centerLatLong: Geographic latitude, longitude of the center point.
							  Represented as a duple.
		@param centerXY: Canvas x and y-coordinates of the center point.
						 Represented as a duple.

		@return: None.
		"""	

		# lat/long of this, where: lat/long of center -> (0,0)
		x1 = self.latitude - centerLatLong[0]
		y1 = self.longitude - centerLatLong[1]

		# scale
		x1 *= scale
		y1 *= scale

		# rotate so plane faces top of canvas
		xRotate = x1 * math.cos(rotation) - y1 * math.sin(rotation)
		yRotate = x1 * math.sin(rotation) + y1 * math.cos(rotation)  # shouldn't this all by y1?

		# translate so that center is in middle of canvas
		self.x = xRotate + centerXY[0]
		self.y = yRotate + centerXY[1]


	def rotate( self , angle , center ) :
		"""
		Rotates this point, clockwise, by the specified angle with respect to the specified center point.
		
		This uses the algorithm for calculating rotation in 2-dimensions (euclidian), where:
		x' = xcos(theta) - ysin(theta)
	 	y' = xsin(theta) + ycos(theta)

		@param angle: The angle this point is to be rotated clockwise by, in radians.
		@param center: The center point which this point is rotated with respect to.
					   Represented as a duple.

		@return: None.
		"""	
	 	x1 = self.x - center[0]
	 	y1 = self.y - center[1]

	 	xNew = x1 * math.cos(angle) - y1 * math.sin(angle)
	 	yNew = x1 * math.sin(angle) + y1 * math.cos(angle)

	 	self.x = xNew + center[0]
	 	self.y = yNew + center[1]


	# --- Painting ------------------------------------------------ #
	
	def paint( self , canvas , scale , rotation , centerLatLong , centerXY ) :
		"""
		Calculates the canvas coordinates of this point and paints it onto the canvas.
		
		@param canvas: The canvas this point is to be drawn onto.
		@param scale: Magnitude of the scale required to convert geographic coordinates to canvas coordinates.
		@param rotation: The angle, in radians, from North that this point is to be rotated by, in a clockwise direction, relative to the center point.
		@param centerLatLong: Geographic latitude, longitude of the center point.
							  Represented as a duple.
		@param centerXY: Canvas x and y-coordinates of the center point.
						 Represented as a duple.

		@return: None.
		"""
		if self.toPaint :
			self.calculateXY( scale , rotation , centerLatLong , centerXY )  
			
			# adjust (x,y) so that point is in center of drawn point.
			self.x -= self.weight / 2
			self.y -= self.weight / 2

			canvas.create_line( self.x , self.y , self.x , self.y + self.weight , fill = self.colour , width = self.weight )


	# --- Setters ------------------------------------------------- #

	def setPaint( self , toPaint ) :
		"""
		Sets this point to paint or not.
		@param toPaint: True if this point is to be painted onto the canvas, False otherwise.
		@return: None.
		"""
		self.toPaint = toPaint 


	# --- Getters ------------------------------------------------- #
	
	def getX( self ) :
		"""
		Returns the canvas x-coordinate of this point.
		@return: The canvas x-coordinate of this point.
		"""
		return self.x


	def getY( self ) :
		"""
		Returns the canvas y-coordinate of this point.
		@return: The canvas y-coordinate of this point.
		"""
		return self.y


	def getCanvasPt( self ) :
		"""
		Returns the canvas coordinates of this point as a duple. (x,y)
		@return: The canvas coordinates of this point as a duple. (x,y)
		"""
		return ( self.x , self.y )


	def getLatitude( self ) :
		"""
		Returns the latitude value of this point.
		@return: The latitude value of this point.
		"""
		return self.latitude 


	def getLongitude( self ) :
		"""
		Returns the longitude value of this point.
		@return: The longitude value of this point.
		"""
		return self.longitude
