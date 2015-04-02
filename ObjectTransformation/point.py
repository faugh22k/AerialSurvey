import math

class PointPolar() :
	"""
	a point, in polar coordinate wrt center of canvas
	(i,j,theta)
	"""

	# Geographic latitude, longitude values of this point
	latitude = None
	longitude = None
	
	# i,j (width,height) distances wrt to (0,0) of canvas
	i = None
	j = None


	def __init__( self , geoPt ,  ) :
		"""
		Constructor

		@param geoPt: Geographic latitude , longitude of this point
		@param
		"""
		self.latitude = latitude
		self.longitude = longitude
		




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
