from Tkinter import *		# for drawing
import math					# for calculations

from point import Point 	# Line uses 2 Points


class Line() :
	"""
	A Line.

	@author: Elizabeth Fong, Kim Faughnan, Spring 2015
	"""

	# line drawing variables
	colour = None
	weight = None

	# the 2 points of a line (start,end)
	point1 = None
	point2 = None


	# --- Constructor --------------------------------------------- #

	def __init__( self , geoPt1 , geoPt2 , lineColour , lineWeight ) :
		"""
		Constructor: Initialises this line.

		@param geoPt1: Geographic latitude, longitude of the start point of this line.
					   Represented as a duple.
		@param geoPt2: Geographic latitude, longitude of the end point of this line.
					   Represented as a duple.
		@param lineColour: The colour of this line.
		@param lineWeight: The weight of this line.

		@return: None.
		"""
		self.point1 = Point( geoPt1 , None , None )
		self.point2 = Point( geoPt2 , None , None )

		self.colour = lineColour
		self.weight = lineWeight


	# --- Transformation ------------------------------------------ #

	def calculateXY( self , scale , rotation , centerLatLong , centerXY ) :
		"""
		Calculates the canvas coodinates of this line.

		@param scale: Magnitude of the scale required to convert geographic coordinates to canvas coordinates.
		@param rotation: The angle, in radians, from North that this line is to be rotated by, in a clockwise direction, relative to the center point.
		@param centerLatLong: Geographic latitude, longitude of the center point.
							  Represented as a duple.
		@param centerXY: Canvas x and y-coordinates of the center point.
						 Represented as a duple.

		@return: None.
		"""
		self.point1.calculateXY( scale , rotation , centerLatLong , centerXY )
		self.point2.calculateXY( scale , rotation , centerLatLong , centerXY )


	# --- Painting ------------------------------------------------ #

	def paint( self , canvas , scale , rotation , centerLatLong , centerXY ) : 
		"""
		Calculates the canvas coordinates of this line and paints it onto the canvas.

		@param canvas: The canvas this line is to be drawn on.
		@param scale: Magnitude of the scale required to convert geographic coordinates to canvas coordinates.
		@param rotation: The angle, in radians, from North that this line is to be rotated by, in a clockwise direction, relative to the center point.
		@param centerLatLong: Geographic latitude, longitude of the center point.
							  Represented as a duple.
		@param centerXY: Canvas x and y-coordinates of the center point.
						 Represented as a duple.

		@return: None.
		"""
		self.calculateXY( scale , rotation , centerLatLong , centerXY ) 
		self.drawLine()


	def paintPlaneLine( self , canvas , rotation , centerXY ) :
		"""
		Rotates and paints this line as part of the representation of a plane onto the canvas.
		This method is only called if this line is a plane line.

		@param canvas: The canvas this line is to be drawn on.
		@param rotation: The angle, in radians, from North that this line is to be rotated by, in a clockwise direction, relative to the center point.
		@param centerXY: Canvas x and y-coordinates of the center point.
						 Represented as a duple.

		@return: None.
		"""
		self.point1.rotate( rotation , centerXY )
		self.point2.rotate( rotation , centerXY )
		self.drawLine()


	def drawLine( self , canvas ) :
		"""
		Paints this line onto the given canvas.
		@param canvas: The canvas this line is to be drawn on.
		@return: None.
		"""
		canvas.create_line( self.point1.getX() , self.point1.getY() , self.point2.getX() , self.point2.getY() , fill = self.colour , width = self.weight )


	# --- Getters ------------------------------------------------- #

	def getAngle( self ) :
		"""
		Calculates and returns the clockwise angle, in radians, from North this line has.
		The calculation assumes that point1 is the start point and point2 is the end point.

		@return: The clockwise angle from North this line has, in radians.
		"""
		# positive y is in the North direction
		deltaX = self.point2.getX() - self.point1.getX()
		deltaY = self.point1.getY() - self.point2.getY()
		return math.atan2( deltaX , deltaY )


	def getPoints(self):
		"""
		Returns the 2 end points of this line as a duple, in the format (point1,point2).
		@return: The 2 end points of this line as a duple, in the format (point1,point2).
		"""
		return (self.point1, self.point2)
