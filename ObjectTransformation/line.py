from Tkinter import *
from point import Point

import math

class Line() :
	"""
	a line
	"""

	colour = None
	weight = None

	point1 = None
	point2 = None

	# angle, in radians
	angle = None


	translateX = None
	translateY = None

	scale = None

	rotation = None


	# --- Constructor --------------------------------------------- #

	def __init__( self , geoPt1 , geoPt2 , lineColour , lineWeight ) :
		"""
		Constructor

		@param geoPt1: Geographic latitude, longitude of the start point of this line
		@param geoPt2: Geographic latitude, longitude of the end point of this line.
		"""
		self.point1 = Point( geoPt1 , None , None )
		self.point2 = Point( geoPt2 , None , None )

		self.colour = lineColour
		self.weight = lineWeight

		# calculating line angle - y-axis faces top
		deltaX = self.point2.getX() - self.point1.getX()
		deltaY = self.point1.getY() - self.point2.getY()
		self.angle = math.atan2( deltaX , deltaY )


	# --- Transformation Methods ---------------------------------- #

	def calculateXY( self , scale , rotation , centerLatLong , centerXY ) :
		self.point1.calculateXY( scale , rotation , centerLatLong , centerXY )
		self.point2.calculateXY( scale , rotation , centerLatLong , centerXY )


	# def rotate( self , rotation , center ) :
	# 	"""
	# 	Rotate about a certain point, center
	# 	@param rotation: the angle to rotate this line with, in radians
	# 	@param center: The point to rotate this line about
	# 	"""
	# 	self.angle += rotation

	# 	self.point1.rotate( rotation , center )
	# 	self.point2.rotate( rotation , center )


	# def scale( self , factor , center ) :
	# 	self.point1.scale( factor , center )
	# 	self.point2.scale( factor , center )
		

	# def translate( self , factorX , factorY ) :
	# 	self.point1.translate( factorX , factorY )
	# 	self.point2.translate( factorX , factorY )


	# --- Others -------------------------------------------------- #

	def paint( self , canvas , scale , rotation , centerLatLong , centerXY ) : 
		self.calculateXY( scale , rotation , centerLatLong , centerXY ) 
		self.drawLine()

	def paintPlaneLine( self , canvas , rotation , centerXY ) :
		self.point1.rotate( rotation , centerXY )
		self.point2.rotate( rotation , centerXY )
		self.drawLine()

	def drawLine( self , canvas ) :
		canvas.create_line( self.point1.getX() , self.point1.getY() , self.point2.getX() , self.point2.getY() , fill = self.colour , width = self.weight )

	# --- Getters ------------------------------------------------- #

	def getAngle( self ) :
		return self.angle 


	def getPoints(self):
		return (self.point1, self.point2)



