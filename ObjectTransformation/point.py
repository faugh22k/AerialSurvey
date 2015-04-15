from Tkinter import *
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


	def __init__( self , geoPt , ptColour , ptWeight ) :
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

		self.x = geoPt[0]
		self.y = geoPt[1]

		self.colour = ptColour
		self.weight = ptWeight


	# --- Transformation Methods ---------------------------------- #

	def rotate( self , angle , center ) :
		# using rotation in 2-dimensions (euclidian)
		# x' = xcos(theta) - ysin(theta)
		# y' = xsin(theta) + ycos(theta)
		
		x1 = self.x - center[0]
		y1 = self.y - center[1]

		xNew = x1 * math.cos(angle) - y1 * math.sin(angle)
		yNew = x1 * math.sin(angle) + y1 * math.cos(angle)

		self.x = xNew + center[0]
		self.y = yNew + center[1]


	def scale( self , magnitude , center ) :
		"""
		@param magnitude :
		@param center :
		"""
		# scale distance between center and point
		x1 = self.x - center[0]
		y1 = self.y - center[1]

		xNew = x1 * magnitude
		yNew = y1 * magnitude

		self.x = xNew + center[0]
		self.y = yNew + center[1]


	def translate( self , factorX , factorY ) :
		"""
		@param factorX :
		@param factorY :
		"""
		self.x += factorX
		self.y += factorY


	# --- Others -------------------------------------------------- #
	
	def paint( self , canvas ) :
		print("...\npoint: {0}, {1}".format(self.x, self.y))
		canvas.create_line( self.x , self.y , self.x , self.y + self.weight , fill = self.colour , width = self.weight )


	# --- Getters ------------------------------------------------- #
	
	def getX( self ) :
		return self.x

	def getY( self ) :
		return self.y

	def getCanvasPt( self ) :
		return ( self.x , self.y )

	def getLatitude( self ) :
		return self.latitude 

	def getLongitude( self ) :
		return self.longitude

