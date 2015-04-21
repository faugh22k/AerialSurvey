from Tkinter import *
import tkMessageBox
from preflightMode import *
from navigationManager import *


class AerialSurveyApplication(Frame):

	rampsFileName = None
	linesFileName = None

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

	preflightMode = None
	navigationManager = None


	def __init__(self):
		Frame.__init__(self, None)
		self.pack()
		self.preflightMode = PreFlightMode(self, self)

	def leavePreFlightMode(self):
		print ("leave pre flight mode")

		try:
			flightplanWeight = self.preflightMode.getFlightlinesWeight()
			breadcrumbsWeight = self.preflightMode.getBreadcrumbsWeight()

			if (flightplanWeight <= 0 or breadcrumbsWeight <= 0):
				raise ValueError
		except ValueError:
			tkMessageBox.showinfo("Please Review Your Selections", "Drawing weights must be integers more than or equal to 1.")
			return

		self.linesFileName = self.preflightMode.getFlightrampsFile()
		self.rampsFileName = self.preflightMode.getFlightlinesFile()

		if (self.linesFileName == "" or self.rampsFileName == ""):
			tkMessageBox.showinfo("Please Review Your Selections", "Please select both Ramps and Flightlines Files.")
			return
 		     
		self.colour_flightlines = self.preflightMode.getColorFlightlines()
		self.colour_ramps = self.preflightMode.getColorRamps()
		self.colour_breadcrumbs = self.preflightMode.getColorBreadcrumbs()
		self.colour_background = self.preflightMode.getColorBackground()

		

		self.switchModes()

	def switchModes(self):
		self.preflightMode.remove()
		#self.preflightMode.pack_forget() 
		#self.preflightMode.destroy() 
		self.navigationManager = NavigationManager(self, self.canvas_width, self.canvas_height, self.linesFileName, self.rampsFileName, self.colour_flightlines, self.colour_ramps, self.colour_breadcrumbs, self.colour_background, self.weight_flightplan, self.weight_breadcrumbs)
		self.pack()



 

if __name__ == "__main__":
    # Starts the program.
    aerialSurveyApplication = AerialSurveyApplication() 
    aerialSurveyApplication.mainloop() 




