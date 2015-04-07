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
colour_breadcrumbs = "00cc00"

# other constants
weight = 3
default_scale = 100000
default_translateX = 32257300
default_translateY = 20774500


# breadcrumbs - around -72.5753726146, 42.2553932356 +- 0.000001
breadcrumbs = ( Point( (-72.5753720000,42.2553930000) , center , colour_breadcrumbs , weight ) )


# MAIN
canvas = Canvas( master , width = canvas_width , height = canvas_height )
canvas.pack()

scale = default_scale
translateX = default_translateX
translateY = default_translateY




# flightlines
campusSHP = shapefile.Reader( file_flightlines )
shapes = campusSHP.shapes()

for shape in shapes:
	points = shape.points
	line = Line( points[0] , points[1] , colour_flightlines , weight )

	line.scale( scale , breadcrumbs[-1] )
	line.translate( translateX , translateY )

	line.paint( canvas )

# ramps
campusSHP = shapefile.Reader( file_ramps )
shapes = campusSHP.shapes()

for shape in shapes:
	points = shape.points
	line = Line( points[0] , points[1] , colour_ramps , weight )

	line.scale( scale , breadcrumbs[-1] )
	line.translate( translateX , translateY )

	line.paint( canvas )