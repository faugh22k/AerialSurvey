from pynmea.pynmea import nmea

import pyserial.serial as serial, time, sys, threading, datetime, shutil
import pyserial.serial.serialutil as serialutil
import pyserial.serial.serialwin32 as serialwin32


class GPSReader():
	"""
	GPS Reader for reading GPS data.

	@author: Kim Faughnan, Elizabeth Fong, Spring 2015
	"""

	# gpgga - for geographic lat, long
	gpggaBAUDRATE = None  
	gpggaComnum = None
	gpggaSerial = None

	# gpvtg - for ground speed and bearing
	gpvtgBAUDRATE = None  
	gpvtgComnum = None
	gpvtgSerial = None

	# current position (longitude,latitude)
	currentPosition = None


	# --- Construction -------------------------------------------- #

	def __init__(self, gpggaComnum="COM1", gpggaBaudrate=4800, gpvtgComnum="COM2", gpvtgBaudrate=4800): 
		"""
		Constructor: Initialises the GPS reader.

		@return: None.
		"""
		self.gpggaBAUDRATE = gpggaBaudrate
		self.gpggaComnum = gpggaComnum

		self.gpvtgBAUDRATE = gpvtgBaudrate 
		self.gpvtgComnum = gpvtgComnum 


	def initConnections(self): 
		"""
		Initialises connections to the bluetooth GPS.

		@return: None.
		"""
		# init gpggaSerial
		self.gpggaSerial = serialwin32.Serial()
		self.gpggaSerial.baudrate = self.gpggaBAUDRATE
		self.gpggaSerial.port = self.gpggaComnum
		self.gpggaSerial.timeout = 1
		self.gpggaSerial.open()
		self.gpggaSerial.isOpen() 
	
		print 'OPEN: '+ self.gpggaSerial.name
		print '' 

		# init gpvtgSerial
		self.gpvtgSerial = serialwin32.Serial()
		self.gpvtgSerial.baudrate = self.gpvtgBAUDRATE
		self.gpvtgSerial.port = self.gpvtgComnum
		self.gpvtgSerial.timeout = 1
		self.gpvtgSerial.open()
		self.gpvtgSerial.isOpen()  
	
		print 'OPEN: '+ self.gpvtgSerial.name
		print '' 


	# --- Read GPS Data ------------------------------------------- #

	def getLongLat(self):
		"""
		Returns the geographic coordinates as a duple, in the format (longitude,latitude).
		
		@return The geographic coordinates, (longitude,latitude).
		"""
		try:
			# read line
			lastLine = "0" 
			line = "0" 
			while line is not "" or (lastLine is "0" or lastLine is ""):
				print("lastLine was {0}".format(line))
				lastLine = line
				line = self.gpggaSerial.readline()   
			print("\n      after line read.")    

			line = lastLine
			print "   from gps: ", line  
			
			# parse line in NMEA GPGGA format
			gpgga = nmea.GPGGA() 
			gpgga.parse(line)

			# example gpgga format line:
			#    $GPGGA,070010.5,4215.35012,N,07234.49672,W,2,15,0.7,85.1,M,-33.0,M,,*57
			#                    4215.35012,N,07234.49672,W
			#                    42 degrees N, -72 degrees W 

			lats = gpgga.latitude
			longs = gpgga.longitude 
			
			#convert degrees,decimal minutes to decimal degrees 
			lat1 = (float(lats[2]+lats[3]+lats[4]+lats[5]+lats[6]+lats[7]+lats[8]))/60
			lat = (float(lats[0]+lats[1])+lat1)
			long1 = (float(longs[3]+longs[4]+longs[5]+longs[6]+longs[7]+longs[8]+longs[9]))/60
			long = (float(longs[0]+longs[1]+longs[2])+long1)
			
			#calculate position 
			pos_y = lat
			pos_x = -long 	#longitude is negative  

			#shows that we are reading through this loop
			print ("x: %f"  % pos_x)
			print ("y: %f"  % pos_y) 

			self.currentPosition = (pos_x,pos_y)
			return (pos_x,pos_y)

		except:
			print "error in stream_serial ", sys.exc_info()[0]
			pass 


	def getGroundSpeedAndBearing(self):
		"""
		Returns the ground speed and bearing read from the GPS, as a duple, with the format
		(ground speed, bearing).

		@return: The ground speed and bearing.
		"""
		try:
			# read line
			lastLine = "0" 
			line = "0" 
			while line is not "" or (lastLine is "0" or lastLine is ""):
				print("lastLine was {0}".format(line))
				lastLine = line
				line = self.gpvtgSerial.readline()   
			print("\n      after line read.")    
			
			line = lastLine
			print "   from gps: ", line  
			
			# parse line in NMEA GPVTG format
			gpvtg = nmea.GPVTG() 
			gpvtg.parse(line)

			# example gpvtg format line:
			#    $gpvtg,070010.5,4215.35012,N,07234.49672,W,2,15,0.7,85.1,M,-33.0,M,,*57
			#                    4215.35012,N,07234.49672,W
			#                    42 degrees N, -72 degrees W 

			bearing = gpvtg.true_track #or mag_track
			groundspeed = gpvtg.spd_over_grnd_kmph #or for knots end with kts instead of kmph  
			print ("returning {0} from ground speed bearing".format((groundspeed,bearing)))
			
			return (groundspeed,bearing)

		except:
			print "error in stream_serial ", sys.exc_info()[0]
			pass  
