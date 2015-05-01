from point import *
from line import *
#from gpsData import GPS

class Breadcrumbs() : 

	path = None

	pointSize = 5
	pointColor = "#135e1c" 

	# breadcrumb drawing frequency - once every n points read from GPS
	drawingFreq = 3

	# plane size - for drawing (magnitude of dist from center pt to front tip pt)
	planeSize = 6
	planeColour = "#000000"
	planeWeight = 3 


	def __init__( self, pointColor, pointSize, planeColor ) :
		self.path = [] 

		self.pointColor = pointColor
		self.pointSize = pointSize 
		self.planeColor = planeColor

		# for initial test data
		#self.path = [Point((-72.5753720000,42.2553930000), self.pointColor, self.pointSize) , Point((-72.5753735000,42.2553950000), self.pointColor, self.pointSize)]
		#self.path = [Point((20,20), self.pointColor, self.pointSize) , Point((30,25), self.pointColor, self.pointSize), Point((0,0), self.pointColor, self.pointSize), Point((250,400), self.pointColor, self.pointSize)]

	def addPoint( self , point ) :

		#prev = self.path[-1]

		# for dashed lines or dots with even intervals - need to determine length, lines drawn accordingly
		# angle between vectors: v dot w = |v| |w| cos(theta)

		adding = Point(point, self.pointColor, self.pointSize)
		self.path.append( adding )  
		if len(self.path)%self.drawingFreq != 0:
			adding.toPaint = False

	def translate(self, x, y):
		for point in self.path:
			point.translate(x,y)

	def scale(self, magnitude, center):
		for point in self.path:
			point.scale(magnitude, center)

	def clear(self):
		for point in self.path:
			point.toPaint = False


	# --- PAINT FUNCTIONS ----------------------------------------- #

	def paint( self , canvas , scale , rotation , centerLatLong , centerXY ) :
		print("  painting breadcrumbs")
		# draws every third point, starting from the most recently added
		pointNumber = 0
		for point in reversed(self.path):
			if pointNumber % self.drawingFreq == 0: 
				point.paint(canvas , scale , rotation , centerLatLong , centerXY )  
			pointNumber += 1

		# painting plane
		adjustedCenter = ( centerXY[0] - self.pointSize/2 , centerXY[1] - self.pointSize/2 )
		self.drawPlane( canvas , rotation , adjustedCenter )


	def drawPlane( self , canvas , rotation , centerXY ) :
		# plane: a set of 3 lines
		# draw as if rotation is 0 , then rotate before painting
		centerX = centerXY[0]
		centerY = centerXY[1]

		tip = ( centerX , centerY-self.planeSize )
		left = ( centerX-self.planeSize , centerY+self.planeSize )
		right = ( centerX+self.planeSize , centerY+self.planeSize )

		line1 = Line( tip , left , self.planeColour , self.planeWeight )
		line2 = Line( tip , right , self.planeColour , self.planeWeight )
		line3 = Line( left , right , self.planeColour , self.planeWeight )

		line1.paintPlaneLine( canvas , rotation , centerXY )
		line2.paintPlaneLine( canvas , rotation , centerXY )
		line3.paintPlaneLine( canvas , rotation , centerXY )

