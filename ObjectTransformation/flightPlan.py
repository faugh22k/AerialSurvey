
import shapefile  
from line import * 


class FlightPlan():

	canvas = None
	lineColor = None#"#ffff33"
	rampColor = None#"#ff0000"
	drawingWidth = None#2

	def __init__(self, fileNameLines, fileNameRamps, lineColor, rampColor, drawingWidth, canvas): 
		lines = shapefile.Reader(fileNameLines)
		ramps = shapefile.Reader(fileNameRamps)

		self.canvas = canvas

		self.lineColor = lineColor
		self.rampColor = rampColor
		self.drawingWidth = drawingWidth

		self.lines = []
		self.ramps = [] 

		# for testing
		#self.lines.append( Line( (30,40), (50, 60), self.lineColor, self.drawingWidth)) 
		#self.lines.append( Line( (310,410), (510, 610), self.lineColor, self.drawingWidth)) 

		#self.ramps.append( Line( (25,35), (30,40), self.rampColor, self.drawingWidth))  
		#self.ramps.append( Line( (305,405), (310,410), self.rampColor, self.drawingWidth))  
		print("^^^")
		for shape in lines.shapes(): 
			points = shape.points
			print("line: {0}".format(points))
			self.lines.append(Line((points[0][0] , points[0][1]) , (points[1][0] , points[1][1]), self.lineColor, self.drawingWidth))  
		print("**********")
		for shape in ramps.shapes(): 
			points = shape.points
			print("ramp: {0}".format(points))
			self.ramps.append(Line((points[0][0] , points[0][1]) , (points[1][0] , points[1][1]), self.rampColor, self.drawingWidth))  
		print("^^^")
		self.getWidthHeight()


	def getWidthHeight(self):

		minX = float("inf")  
		maxX = float("-inf")  
		minY = float("inf") 
		maxY = float("-inf") 

		print("     ^^^^     ")
		for shape in self.lines:
			points = shape.getPoints()  

			for point in points:
				minX = min(point.x, minX)
				maxX = max(point.x, maxX)

				minY = min(point.y, minY)
				maxY = max(point.y, maxY)
				print("      point: {0}    {1}".format(point.x, point.y)) 

		for shape in self.ramps:
			points = shape.getPoints()  

			for point in points:
				minX = min(point.x, minX)
				maxX = max(point.x, maxX)

				minY = min(point.y, minY)
				maxY = max(point.y, maxY)
				print("      point: {0}    {1}".format(point.x, point.y))

		self.width = maxX - minX	
		self.height = maxY - minY

		self.minX = minX
		self.minY = minY 

		print("\nin getWidthHeight")
		print("   minX: {0}\n   maxX: {1}".format(minX, maxX))
		print("   minY: {0}\n   maxY: {1}".format(minY, maxY))
		print("   width: {0}\n   height: {1}".format(self.width, self.height))

		return (self.width, self.height)

	def calculateInitialScale(self, canvasWidth, canvasHeight):
		#dimensions = self.getWidthHeight()

		widthRatio = canvasWidth/self.width
		heightRatio = canvasHeight/self.height

		print("\nin calculateInitialScale: ")
		print("   canvasWidth: {0}\n   canvasHeight: {1}\n   width: {2}\n   height: {3}".format(canvasWidth, canvasHeight, self.width, self.height))
		print("   widthRatio: {0}\n   heightRatio: {1}\n   chosenRatio: {2}".format(widthRatio, heightRatio, min(widthRatio,heightRatio)))
		return min(widthRatio, heightRatio) 

	def getInitialTranslation(self):
		return (self.minX, self.minY)

	def getInitialCenter(self):
		return (self.minX + (self.width/2), self.minY + (self.height/2)) 

	# def scale(self, scale, origin):
	# 	for item in self.lines:
	# 		item.scale(scale, origin) 

	# 	for item in self.ramps: 
	# 		item.scale(scale, origin)  

	# def translate(self, x, y):
	# 	for item in self.lines:
	# 		item.translate(x,y)

	# 	for item in self.ramps:
	# 		item.translate(x,y)

	def paint(self, canvas , scale , rotation , centerLatLong , centerXY ):
		print("  painting flight plan") 
		  
		for item in self.ramps: 
			item.paint(self.canvas , scale , rotation , centerLatLong , centerXY ) 

		for item in self.lines:
			item.paint(self.canvas , scale , rotation , centerLatLong , centerXY )



