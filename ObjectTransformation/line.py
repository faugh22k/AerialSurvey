from Tkinter import *
from point import PointCartesian
from point import Point

import math

class Line() :
	"""
	a line - uses polar coordinates
	"""

	colour = None
	weight = None

	point1 = None
	point2 = None

	# angle, in radians
	angle = None


	# --- Constructor --------------------------------------------- #

	def __init__( self , geoPt1 , geoPt2 , lineColour , lineWeight ) :
		"""
		Constructor

		@param geoPt1: Geographic latitude, longitude of the start point of this line
		@param geoPt2: Geographic latitude, longitude of the end point of this line.
		"""
		self.point1 = Point( geoPt1 , geoPt1 , None , None )
		self.point2 = Point( geoPt2 , geoPt1 , None , None )

		self.colour = lineColour
		self.weight = lineWeight

		# calculating line angle
		deltaX = self.point2.getX() - self.point1.getX()
		deltaY = self.point2.getY() - self.point1.getY()
		self.angle = math.atan2( deltaX , deltaY )


	# --- Transformation Methods ---------------------------------- #

	def rotate( self , rotation , center ) :
		"""
		Rotate about a certain point, center
		@param rotation: the angle to rotate this line with, in radians
		@param center: The point to rotate this line about
		"""
		self.angle += rotation

		self.point1.rotate( rotation , center )
		self.point2.rotate( rotation , center )


	def scale( self , factor , center ) :
		self.point1.scale( factor , center )
		self.point2.scale( factor , center )
		

	def translate( self , factorX , factorY ) :
		self.point1.translate( factorX , factorY )
		self.point2.translate( factorX , factorY )


	# --- Others -------------------------------------------------- #

	def paint( self , canvas ) :
		canvas.create_line( self.point1.x() , self.point1.y() , self.point2.x() , self.point2.y() , fill = self.colour , width = self.weight )


	# --- Getters ------------------------------------------------- #

	def angle( self ) :
		return self.angle 

		



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