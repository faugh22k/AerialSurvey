from Tkinter import *
from point import PointCartesian
from point import PointPolar

import math

class LinePolar() :
	"""
	a line - uses polar coordinates
	"""

	origin = None

	point1 = None
	point2 = None

	# angle, in radians
	angle = None



class LineCartesian() :
	"""
	a line
	"""

	point1 = None
	point2 = None


	# --- Constructor --------------------------------------------- #

	def __init__( self , x1 , y1 , x2 , y2 ) : 
		self.point1 = PointCartesian( x1 , y1 )
		self.point2 = PointCartesian( x2 , y2 )
		print( "Points = (" + str(self.point1.getX()) + "," + str(self.point1.getY()) + ") , (" + str(self.point2.getX()) + "," + str(self.point1.getY()) + ")" )


	#def __init__( self , point1 , point2 ) :
	#	self.point1 = point1
	#	self.point2 = point2


	# --- Transformation Methods ---------------------------------- #

	def rotate( self , angle , origin ) :
		self.point1.rotate( angle , origin )
		self.point2.rotate( angle , origin )


	def scale( self , magnitude , origin ) :
		# scale distance between origin and point
		self.point1.scale( magnitude , origin )
		self.point2.scale( magnitude , origin )


	def translate( self , factorX , factorY ) :
		self.point1.translate( factorX , factorY )
		self.point2.translate( factorX , factorY )
		print( "Translation = (" + str(self.point1.getX()) + "," + str(self.point1.getY()) + ") , (" + str(self.point2.getX()) + "," + str(self.point1.getY()) + ")" )


	# --- Drawing ------------------------------------------------- #

	def drawSolidLine( self , canvas , colour , weight ) :
		canvas.create_line( self.point1.getX() , self.point1.getY() , self.point2.getX() , self.point2.getY() , fill = colour , width = weight )


	# --- Others -------------------------------------------------- #

	def length( self ) :
		xDiff = self.point2.getX() - self.point1.getX() 
		yDiff = self.point2.getY() - self.point1.getY()

		return math.sqrt( math.pow(xDiff,2) + math.pow(yDiff,2) )


	def angle( self ) :
		# determine angle between point 1 and point 2 (radians)
		return 1