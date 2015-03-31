import math

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

	def rotate( self , angle , origin ) :
		"""
		@param angle : the angle to rotate by, in radians
		@param origin : center of canvas - a Point object
		"""
		# using rotation in 2-dimensions (euclidian)
		# x' = xcos(theta) - ysin(theta)
		# y' = xsin(theta) + ycos(theta)
		
		x1 = self.x - origin.getX()
		y1 = self.y - origin.getY()

		xNew = x1 * math.cos(angle) - y1 * math.sin(angle)
		yNew = x1 * math.sin(angle) + y1 * math.cos(angle)

		self.x = xNew + origin.getX()
		self.y = yNew + origin.getY()

		print( "rotate - new coordinates = (" + str(self.x) + "," + str(self.y) + ")" )


	def scale( self , magnitude , origin ) :
		"""
		@param magnitude :
		@param origin :
		"""
		# scale distance between origin and point
		x1 = self.x - origin.getX()
		y1 = self.y - origin.getY()

		xNew = x1 * magnitude
		yNew = y1 * magnitude

		self.x = xNew + origin.getX()
		self.y = yNew + origin.getY()

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
