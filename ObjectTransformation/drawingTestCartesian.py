from Tkinter import *
import math

from point import PointCartesian
from line import LineCartesian
from breadcrumbs import BreadcrumbsCartesian

import shapefile

master = Tk()

# constants
canvas_width = 500
canvas_height = 500

scale = 100000
translateX = 32257300
translateY = 20774500

origin = PointCartesian( canvas_width/2 , canvas_height/2 )

# main
canvas = Canvas( master , width = canvas_width , height = canvas_height )
canvas.pack()

campusSHP = shapefile.Reader("campus/test_flightlines.shp")
shapes = campusSHP.shapes()

# flight lines
for shape in shapes:
	points = shape.points
	line = LineCartesian( points[0][0] , points[0][1] , points[1][0] , points[1][1] )
	
	line.scale(scale,origin)
	line.translate(translateX,translateY)

	print( "line length = " + str(line.length()) ) 
	line.drawSolidLine( canvas,"#ffff33" , 2 )

# ramps 
campusRamps = shapefile.Reader("campus/ramps.shp")
shapes = campusRamps.shapes()

for shape in shapes:
	points = shape.points
	line = LineCartesian( points[0][0] , points[0][1] , points[1][0] , points[1][1] )
	
	line.scale(scale,origin)
	line.translate(translateX,translateY)

	print( "line length = " + str(line.length()) ) 
	line.drawSolidLine(canvas,"#ff0000" , 2 )

# breadcrumbs
breadcrumbs = BreadcrumbsCartesian()

breadcrumbs.addPoint(PointCartesian(5,10))
breadcrumbs.drawLatestPoint(canvas)
breadcrumbs.addPoint(PointCartesian(15,20)) 
breadcrumbs.drawLatestPoint(canvas)
breadcrumbs.addPoint(PointCartesian(30,40)) 
breadcrumbs.drawLatestPoint(canvas)

# required to run
mainloop()