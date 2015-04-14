from Tkinter import *

from point import Point
from line import Line

import shapefile

# ------------------------------------------------------------ #

master = Tk()

# files
file_flightlines = "campus/test_flightlines.shp"
file_ramps = "campus/ramps.shp"

# canvas constants
canvas_width = 500
canvas_height = 500

center = (canvas_width/2 , canvas_height/2)

# colour constants
colour_canvas = "#ccccff"
colour_ramps = "#cc0000"
colour_flightlines = "#cccc33"
colour_breadcrumbs = "#135e1c"

# other constants
weight = 3
weight_breadcrumbs = 5

default_scale = 100000
default_translateX = 32257300
default_translateY = 20774500

# test breadcrumbs - around -72.5753726146, 42.2553932356 +- 0.000001
testData = [(-72.5753720000,42.2553930000) , (-72.5753735000,42.2553950000)]


# breadcrumbs 
breadcrumbs = [ Point( testData[0] , colour_breadcrumbs , weight_breadcrumbs ) ]


# MAIN
canvas = Canvas( master , width = canvas_width , height = canvas_height )
canvas.pack()

scale = default_scale
translateX = default_translateX
translateY = default_translateY


# center pt
pt = breadcrumbs[-1]
pt.scale( scale , center )

translateX = center[0] - pt.getX()
translateY = center[1] - pt.getY()

pt.translate( translateX , translateY )


# flightlines
campusSHP = shapefile.Reader( file_flightlines )
campusShapes = campusSHP.shapes()

for shape in campusShapes:
	points = shape.points
	line = Line( points[0] , points[1] , colour_flightlines , weight )

	line.scale( scale , center )
	line.translate( translateX , translateY )

	line.paint( canvas )


# ramps
campusSHP = shapefile.Reader( file_ramps )
rampShapes = campusSHP.shapes()

for shape in rampShapes:
	points = shape.points
	line = Line( points[0] , points[1] , colour_ramps , weight )

	line.scale( scale , center )
	line.translate( translateX , translateY )

	line.paint( canvas )


# draw first breadcrumb pt
pt.paint( canvas )


# clear canvas
canvas.delete( "all" )

# next breadcrumb pt
breadcrumbs.append( Point( testData[-1] , colour_breadcrumbs , weight_breadcrumbs ) )

# calculating distance between this and prev point
pt = breadcrumbs[-1]
pt.scale( scale , center )
pt.translate( translateX , translateY )

# auto translate
deltaX = center[0] - pt.getX()
deltaY = center[1] - pt.getY()

# update translateX , translateY
translateX += deltaX
translateY += deltaY

# translate and paint everything
for shape in campusShapes:
	shape.translate( deltaX , deltaY )
	shape.paint( canvas )

for shape in rampShapes:
	shape.translate( deltaX , deltaY )
	shape.paint( canvas )

for breadcrumb in breadcrumbs:
	breadcrumb.translate( deltaX , deltaY )
	breadcrumb.paint( canvas )

# required to run
mainloop()