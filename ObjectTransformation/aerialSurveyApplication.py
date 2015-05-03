from Tkinter import *	# UI
import tkMessageBox		# UI

from preflightMode import *			# pre-flight mode
from navigationManager import *		# in-flight mode


class AerialSurveyApplication(Tk):
	"""
	The Aerial Survey Application (main class)

	@author: Kim Faughnan, Elizabeth Fong, Spring 2015
	"""

	# file path for ramps and flightlines
	rampsFileName = None
	linesFileName = None

	# the canvas
	canvas = None
	canvas_width = 500
	canvas_height = 500

	# colour variables
	colour_background = "#3b98e3"
	colour_breadcrumbs = "#135e1c"
	colour_flightlines = "#ffff33"
	colour_ramps = "#ff0000"

	# weight variables
	weight_breadcrumbs = 5
	weight_flightplan = 2

	# user modes: pre-flight, in-flight
	preflightMode = None
	navigationManager = None


	# --- Construction -------------------------------------------- #

	def __init__(self):
		"""
		Constructor: Initialises the Aerial Survey Application.

		@return: None.
		"""
		Tk.__init__(self)

		# screen dimensions
		w, h = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry("%dx%d+0+0" % (w, h))
		self.canvas_width = w 
		self.canvas_height = 5*h/6

		# pre-flight mode
		self.preflightFrame = Frame(self, width=1000, height=1000)
		
		self.preflightMode = PreFlightMode(self.preflightFrame, self)
		button = Button(self.preflightFrame, text="Enter Flight Mode", command = self.leavePreFlightMode)
		
		# pack components
		self.preflightMode.pack(side=TOP)
		button.pack(side=BOTTOM)
		
		self.preflightFrame.pack(in_=self)


	# --- Mode Switching: Pre-flight -> In-flgiht ----------------- #

	def leavePreFlightMode(self):
		"""
		Event handler for the button when completed pre-flight setup.
		This leaves the pre-flight mode and switches modes to in-flight mode.

		@return: None.
		"""
		print ("leave pre flight mode")

		# error handling for line/point weights
		try:
			flightplanWeight = self.preflightMode.getFlightlinesWeight()
			breadcrumbsWeight = self.preflightMode.getBreadcrumbsWeight()

			if (flightplanWeight <= 0 or breadcrumbsWeight <= 0):
				raise ValueError
		except ValueError:
			tkMessageBox.showinfo("Please Review Your Selections", "Drawing weights must be integers more than or equal to 1.")
			return

		# set line/point weights
		self.weight_flightplan = flightplanWeight
		self.weight_breadcrumbs = breadcrumbsWeight
		print("line weight {0}, breadcrumb weight {1}".format(self.weight_flightplan, self.weight_breadcrumbs))

		# read file paths
		self.linesFileName = self.preflightMode.getFlightrampsFile()
		self.rampsFileName = self.preflightMode.getFlightlinesFile()

		# error handling for file paths
		if (self.linesFileName == "" or self.rampsFileName == ""): 
			tkMessageBox.showinfo("Please Review Your Selections", "Please select both Ramps and Flightlines Files.")
			return
		if (self.linesFileName == self.rampsFileName):
			tkMessageBox.showinfo("Please Review Your Selections", "Please select two separate Ramps and Flightlines Files.")
			return
 		
 		# set colour variables
		self.colour_flightlines = self.preflightMode.getColorFlightlines()
		self.colour_ramps = self.preflightMode.getColorRamps()
		self.colour_breadcrumbs = self.preflightMode.getColorBreadcrumbs()
		self.colour_background = self.preflightMode.getColorBackground()
		self.plane = self.preflightMode.getColorPlane()

		# pre-flight mode -> in-flight mode
		self.switchModes()


	def switchModes(self):
		"""
		Switch modes from pre-flgiht mode to in-flight mode.

		@return: None.
		"""
		# remove pre-flight mode
		self.preflightMode.remove()
		self.preflightMode.pack_forget() 
		self.preflightMode.destroy()

		# remove frame for pre-flight mode 
		self.preflightFrame.pack_forget()
		self.preflightFrame.destroy()
		
		# add navigation manager (in-flight mode)
		self.navigationManager = NavigationManager(self, self.canvas_width, self.canvas_height, self.linesFileName, self.rampsFileName, self.colour_flightlines, self.colour_ramps, self.colour_breadcrumbs, self.colour_plane, self.colour_background, self.weight_flightplan, self.weight_breadcrumbs)
		self.navigationManager.place(in_=self)
		
		# update self and run in-flight mode
		self.update()
		self.navigationManager.run()



# ----------------------------------------------------------------- #
# --- MAIN -------------------------------------------------------- #
#------------------------------------------------------------------ #

if __name__ == "__main__":
    # Starts the program.
    aerialSurveyApplication = AerialSurveyApplication() 
    aerialSurveyApplication.mainloop() 
