
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
		self.lines.append( Line( (30,40), (50, 60), self.lineColor, self.drawingWidth)) 
		self.lines.append( Line( (310,410), (510, 610), self.lineColor, self.drawingWidth)) 

		self.ramps.append( Line( (25,35), (30,40), self.rampColor, self.drawingWidth))  
		self.ramps.append( Line( (305,405), (310,410), self.rampColor, self.drawingWidth))  

		for shape in lines.shapes():
			points = shape.points
			self.lines.append(Line((points[0][0] , points[0][1]) , (points[1][0] , points[1][1]), self.lineColor, self.drawingWidth))  
		
		for shape in ramps.shapes(): 
			points = shape.points
			self.ramps.append(Line((points[0][0] , points[0][1]) , (points[1][0] , points[1][1]), self.rampColor, self.drawingWidth))  


	def getWidthHeight(self):

		minX = float("inf")  
		maxX = float("-inf")  
		minY = float("inf") 
		maxY = float("-inf") 

		for shape in self.lines:
			points = shape.getPoints()  

			for point in points:
				minX = min(point.x, minX)
				maxX = max(point.x, maxX)

				minY = min(point.y, minY)
				maxY = max(point.y, maxY)

		for shape in self.ramps:
			points = shape.getPoints()  

			for point in points:
				minX = min(point.x, minX)
				maxX = max(point.x, maxX)

				minY = min(point.y, minY)
				maxY = max(point.y, maxY)

		width = maxX - minX	
		height = maxY - minY

		self.minX = minX
		self.minY = minY 

		return (width, height)

	def calculateInitialScale(self, canvasWidth, canvasHeight):
		dimensions = self.getWidthHeight()

		widthRatio = canvasWidth/dimensions[0]
		heightRatio = canvasHeight/dimensions[1]

		return min(widthRatio, heightRatio) 

	def getInitialTranslation(self):
		return (self.minX, self.minY)

	def scale(self, scale, origin):
		for item in self.lines:
			item.scale(scale, origin) 

		for item in self.ramps: 
			item.scale(scale, origin)  

	def translate(self, x, y):
		for item in self.lines:
			item.translate(x,y)

		for item in self.ramps:
			item.translate(x,y)

	def paint(self, canvas):
		print("painting flight plan") 
		  
		for item in self.ramps: 
			item.paint(self.canvas) 

		for item in self.lines:
			item.paint(self.canvas)



