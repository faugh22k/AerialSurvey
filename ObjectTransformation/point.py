import math

class Point() :
	"""
	a point, in polar coordinate wrt center of canvas
	(i,j,theta)
	"""
	# for painting
	colour = None
	weight = None

	# Geographic latitude, longitude values of this point
	latitude = None
	longitude = None
	
	# x,y (width,height) distances wrt to (0,0) of canvas
	x = None
	y = None


	def __init__( self , geoPt , canvasPt , ptColour , ptWeight ) :
		"""
		Constructor

		@param geoPt: Geographic latitude , longitude of this point
		@param canvasPt: Initial point on the canvas (x,y)
		@param ptColour: Colour to paint this point with. None if this point is part of a line.
		@param ptWeight: Weight of this point. None if this point is part of a line.
		@param 
		"""
		self.latitude = geoPt[0]
		self.longitude = geoPt[1]

		self.x = canvasPt[0]
		self.y = canvasPt[1]

		self.colour = ptColour
		self.weight = ptWeight


	# --- Transformation Methods ---------------------------------- #

	def rotate( self , angle , center ) :
		# using rotation in 2-dimensions (euclidian)
		# x' = xcos(theta) - ysin(theta)
		# y' = xsin(theta) + ycos(theta)
		
		x1 = self.x - center.getX()
		y1 = self.y - center.getY()

		xNew = x1 * math.cos(angle) - y1 * math.sin(angle)
		yNew = x1 * math.sin(angle) + y1 * math.cos(angle)

		self.x = xNew + center.getX()
		self.y = yNew + center.getY()


	def scale( self , magnitude , center ) :
		"""
		@param magnitude :
		@param center :
		"""
		# scale distance between center and point
		x1 = self.x - center.getX()
		y1 = self.y - center.getY()

		xNew = x1 * magnitude
		yNew = y1 * magnitude

		self.x = xNew + center.getX()
		self.y = yNew + center.getY()


	def translate( self , factorX , factorY ) :
		"""
		@param factorX :
		@param factorY :
		"""
		self.x += factorX
		self.y += factorY


	# --- Others -------------------------------------------------- #
	
	def paint( self , canvas ) :
		canvas.createLine( self.x , self.y , self.x , self.y + self.weight , fill = self.colour , width = self.weight )


	# --- Getters ------------------------------------------------- #
	
	def getX( self ) :
		return self.x

	def getY( self ) :
		return self.y




class PointCartesian() :
	"""
	a point
	"""

	x = None
	y = None


	# --- Constructor --------------------------------------------- #

	def __init__( self , x , y ) :
		"""
		Constructor
		@param x : The x-coordinate
		@param y : The y-coordinate
		"""
		self.x = x
		self.y = y


	# --- Transformation Methods ---------------------------------- #

	def rotate( self , angle , center ) :
		"""
		@param angle : the angle to rotate by, in radians
		@param center : center of canvas - a Point object
		"""
		# using rotation in 2-dimensions (euclidian)
		# x' = xcos(theta) - ysin(theta)
		# y' = xsin(theta) + ycos(theta)
		
		x1 = self.x - center.getX()
		y1 = self.y - center.getY()

		xNew = x1 * math.cos(angle) - y1 * math.sin(angle)
		yNew = x1 * math.sin(angle) + y1 * math.cos(angle)

		self.x = xNew + center.getX()
		self.y = yNew + center.getY()

		print( "rotate - new coordinates = (" + str(self.x) + "," + str(self.y) + ")" )


	def scale( self , magnitude , center ) :
		"""
		@param magnitude :
		@param center :
		"""
		# scale distance between center and point
		x1 = self.x - center.getX()
		y1 = self.y - center.getY()

		xNew = x1 * magnitude
		yNew = y1 * magnitude

		self.x = xNew + center.getX()
		self.y = yNew + center.getY()

		print( "scale - new coordinates = (" + str(self.x) + "," + str(self.y) + ")" )


	def translate( self , factorX , factorY ) :
		"""
		@param factorX :
		@param factorY :
		"""
		self.x += factorX
		self.y += factorY


	# --- Getters ------------------------------------------------- #

	def getX( self ) :
		"""
		@return 
		"""
		return self.x


	def getY( self ) :
		"""
		@return
		"""
		return self.y
