from Tkinter import *
import math

class Point() :
	"""
	a point
	"""
	# for painting
	colour = None
	weight = None
	toPaint = None

	# Geographic latitude, longitude values of this point
	latitude = None
	longitude = None
	
	# x,y (width,height) distances wrt to (0,0) of canvas
	x = None
	y = None


	def __init__( self , geoPt , ptColour , ptWeight ) :
		"""
		Constructor: Initialises this point.

		@param geoPt: Geographic latitude , longitude of this point
		@param canvasPt: Initial point on the canvas (x,y)
		@param ptColour: Colour to paint this point with. None if this point is part of a line.
		@param ptWeight: Weight of this point. None if this point is part of a line.
		"""
		self.latitude = geoPt[0]
		self.longitude = geoPt[1]

		self.x = geoPt[0]
		self.y = geoPt[1]

		self.colour = ptColour
		self.weight = ptWeight
		self.toPaint = True


	# --- Transformation Methods ---------------------------------- #

	def calculateXY( self , scale , rotation , centerLatLong , centerXY ) :
		"""
		Calculates the canvas coordinates of this point.

		@param scale: Magnitude of the scale required to convert geographic coordinates to canvas coordinates.
		@param rotation: The angle, in radians, from North that this point is to be rotated by, in a clockwise direction, relative to the center point.
		@param centerLatLong: Geographic latitude, longitude of the center point.
		@param centerXY: Canvas x and y-coordinates of the center point.
		"""	
		#print("\n\n^^^^^^^^^^^^^^^^^^^^^^^^\nin calculateXY ")

		# lat/long of this, where: lat/long of center -> (0,0)
		x1 = self.latitude - centerLatLong[0]
		y1 = self.longitude - centerLatLong[1]

		#print("   longitude: {0}\n   centerlong: {1}\n   longitude - centerLong: {2}".format(self.longitude, centerLatLong[0],x1))
		#print("   latitude: {0}\n   centerLat: {1}\n   latitude - centerLat: {2}".format(self.latitude, centerLatLong[1],x1))

		# scale
		x1 *= scale
		y1 *= scale

		#print("\n   scale: {0}\n   x1: {1}\n   y1: {2}".format(scale, x1, y1))

		# rotate so plane faces top of canvas
		xRotate = x1 * math.cos(rotation) - y1 * math.sin(rotation)
		yRotate = x1 * math.sin(rotation) + y1 * math.cos(rotation)  # shouldn't this all by y1?

		#print("\n   x1 * math.cos(rotation) - y1 * math.sin(rotation)")
		#print(  "   {0} * {1}      -      {2} * {3}".format(x1,math.cos(rotation),y1,math.sin(rotation))) 
		#print(  "   {0}    -    {1}".format(x1*math.cos(rotation),y1*math.sin(rotation))) 
		#print(  "   {0}".format(x1*math.cos(rotation)-y1*math.sin(rotation))) 

		# translate so that center is in middle of canvas
		self.x = xRotate + centerXY[0]
		self.y = yRotate + centerXY[1]

		##print("\n   xRotate: {0}\n   yRotate: {1}".format(xRotate, yRotate))
		#print("   longitude: {0}\n   latitude: {1}".format(self.longitude, self.latitude))
		#print("   x: {0}\n   y: {1}\n^^^^^^^^^^^^^^^^^^^^^^^^\n".format(self.x, self.y)) 


	def rotate( self , angle , center ) :
		"""
		
		"""
	 	# using rotation in 2-dimensions (euclidian)
	 	# x' = xcos(theta) - ysin(theta)
	 	# y' = xsin(theta) + ycos(theta)
	
	 	x1 = self.x - center[0]
	 	y1 = self.y - center[1]

	 	xNew = x1 * math.cos(angle) - y1 * math.sin(angle)
	 	yNew = x1 * math.sin(angle) + y1 * math.cos(angle)

	 	self.x = xNew + center[0]
	 	self.y = yNew + center[1]

	# def scale( self , magnitude , center ) :
	# 	"""
	# 	MAY BE BROKEN
	# 	@param magnitude :
	# 	@param center :
	# 	"""
	# 	# scale distance between center and point
	# 	x1 = self.x - center[0]
	# 	y1 = self.y - center[1]

	# 	xNew = x1 * magnitude
	# 	yNew = y1 * magnitude

	# 	self.x = xNew + center[0]
	# 	self.y = yNew + center[1]
	


	# def translate( self , factorX , factorY ) :
	# 	"""
	# 	MAY BE BROKEN
	# 	@param factorX :
	# 	@param factorY :
	# 	"""
	# 	self.x += factorX
	# 	self.y += factorY


	# --- Others -------------------------------------------------- #
	
	def paint( self , canvas , scale , rotation , centerLatLong , centerXY ) :
		"""
		Calculates the canvas coordinates of this point and paints it onto the canvas.
		
		@param canvas:
		@param scale:
		@param rotation:
		@param centerLatLong:
		@param centerXY:
		"""
		if self.toPaint :
			self.calculateXY( scale , rotation , centerLatLong , centerXY )  
			
			self.x -= self.weight / 2
			self.y -= self.weight / 2

			canvas.create_line( self.x , self.y , self.x , self.y + self.weight , fill = self.colour , width = self.weight )
			#print("drawing: xy: {0}\n        latLong: {1}".format((self.x,self.y),(self.latitude,self.longitude)))


	# --- Setters ------------------------------------------------- #

	def setPaint( self , toPaint ) :
		"""
		Sets this point to paint or not.
		@param toPaint: True if this point is to be painted onto the canvas, False otherwise.
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
