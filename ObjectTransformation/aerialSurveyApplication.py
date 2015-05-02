from Tkinter import *
import tkMessageBox
from preflightMode import *
from navigationManager import *


class AerialSurveyApplication(Tk):

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

	#outermostFrame = None
	preflightMode = None
	navigationManager = None


	def __init__(self):
		Tk.__init__(self)#, None, width=1000, height=1000) 
		#self.pack() 

		w, h = self.winfo_screenwidth(), self.winfo_screenheight()
		#self.overrideredirect(1)
		self.geometry("%dx%d+0+0" % (w, h))
		#self.w = w
		#self.h = h
		self.canvas_width = w 
		self.canvas_height = 5*h/6

		#self.geometry("700x900")
		self.preflightFrame = Frame(self, width=1000, height=1000)
		
		self.preflightMode = PreFlightMode(self.preflightFrame, self)
		button = Button(self.preflightFrame, text="Enter Flight Mode", command = self.leavePreFlightMode)
		
		self.preflightMode.pack(side=TOP)
		button.pack(side=BOTTOM)
		
		self.preflightFrame.pack(in_=self)

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

		self.weight_flightplan = flightplanWeight
		self.weight_breadcrumbs = breadcrumbsWeight
		print("line weight {0}, breadcrumb weight {1}".format(self.weight_flightplan, self.weight_breadcrumbs))

		self.linesFileName = self.preflightMode.getFlightrampsFile()
		self.rampsFileName = self.preflightMode.getFlightlinesFile()

		if (self.linesFileName == "" or self.rampsFileName == ""): 
			tkMessageBox.showinfo("Please Review Your Selections", "Please select both Ramps and Flightlines Files.")
			return
		if (self.linesFileName == self.rampsFileName):
			tkMessageBox.showinfo("Please Review Your Selections", "Please select two separate Ramps and Flightlines Files.")
			return
 		     
		self.colour_flightlines = self.preflightMode.getColorFlightlines()
		self.colour_ramps = self.preflightMode.getColorRamps()
		self.colour_breadcrumbs = self.preflightMode.getColorBreadcrumbs()
		self.colour_background = self.preflightMode.getColorBackground()
		self.plane = self.preflightMode.getColorPlane()

		

		self.switchModes()

	def switchModes(self):
		self.preflightMode.remove()
		self.preflightMode.pack_forget() 
		self.preflightMode.destroy() 
		self.preflightFrame.pack_forget()
		self.preflightFrame.destroy()
		#self.pack_forget() 
		self.navigationManager = NavigationManager(self, self.canvas_width, self.canvas_height, self.linesFileName, self.rampsFileName, self.colour_flightlines, self.colour_ramps, self.colour_breadcrumbs, self.colour_plane, self.colour_background, self.weight_flightplan, self.weight_breadcrumbs)
		self.navigationManager.place(in_=self)
		#self.pack()
		self.update()
		self.navigationManager.run()



 

if __name__ == "__main__":
    # Starts the program.
    aerialSurveyApplication = AerialSurveyApplication() 
    aerialSurveyApplication.mainloop() 



