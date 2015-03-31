from point import PointCartesian
#from gpsData import GPS

class BreadcrumbsCartesian() :

	path = []

	pointLength = 1

	angle = 0

	def __init__( self ) :
		self.path = []

	def groundSpeed( self ) :
		# calculate ground speed
		return 1

	def addPoint( self , point ) :

		#prev = self.path[-1]

		# for dashed lines or dots with even intervals - need to determine length, lines drawn accordingly
		# angle between vectors: v dot w = |v| |w| cos(theta)

		self.path.append( point )


	def drawLatestPoint( self , canvas ) :
		# draws the most recently-added point
		point = self.path[-1] 
		canvas.create_line( point.getX() , point.getY() , point.getX() , point.getY() + 3 , fill = "#68a83d" , width = 3 )

	def drawDashedLine( self , canvas ) :
		# draws set of points as lines
		return 1

	def drawTmpPlane( self , canvas ) :
		# canvas rotates wrt to plane
		return 1


	def angle( self ) :
		# angle that plane rotated by
		return 1
