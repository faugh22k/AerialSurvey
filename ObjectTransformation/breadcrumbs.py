from point import *
#from gpsData import GPS

class Breadcrumbs() : 

	path = None

	pointSize = 5
	pointColor = "#135e1c" 

	def __init__( self ) :
		self.path = [] 

		# for initial test data
		#self.path = [Point((-72.5753720000,42.2553930000), self.pointColor, self.pointSize) , Point((-72.5753735000,42.2553950000), self.pointColor, self.pointSize)]
		self.path = [Point((20,20), self.pointColor, self.pointSize) , Point((30,25), self.pointColor, self.pointSize), Point((0,0), self.pointColor, self.pointSize), Point((250,400), self.pointColor, self.pointSize)]

	def addPoint( self , point ) :

		#prev = self.path[-1]

		# for dashed lines or dots with even intervals - need to determine length, lines drawn accordingly
		# angle between vectors: v dot w = |v| |w| cos(theta)

		self.path.append( Point(point, self.color, self.pointSize) ) 


	#def drawLatestPoint( self , canvas ) :
	#	# draws the most recently-added point
	#	point = self.path[-1] 
	#	canvas.create_line( point.getX() , point.getY() , point.getX() , point.getY() + 3 , fill = "#68a83d" , width = 3 )


	def translate(self, x, y):
		for point in self.path:
			point.translate(x,y)

	def scale(self, magnitude, center):
		for point in self.path:
			point.scale(magnitude, center)


	def paint( self , canvas ) :
		print("painting breadcrumbs")
		# draws every third point
		pointNumber = 0
		for point in self.path:
			if pointNumber % 3 == 0:
				point.paint(canvas)

	
