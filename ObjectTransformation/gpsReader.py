

from pynmea.pynmea import nmea
#*import matplotlib.pyplot as plt
import pyserial.serial as serial, time, sys, threading, datetime, shutil
import pyserial.serial.serialutil as serialutil
import pyserial.serial.serialwin32 as serialwin32

class GPSReader():

	ser = None
	
	#lat = None
	#long = None
	#pos_x = None
	#pos_y = None 


	gpggaBAUDRATE = None  
	gpggaComnum = None
	gpggaSerial = None

	gpvtgBAUDRATE = None  
	gpvtgComnum = None
	gpvtgSerial = None

	currentPosition = None


	def __init__(self, gpggaComnum="COM1", gpggaBaudrate=4800, gpvtgComnum="COM2", gpvtgBaudrate=4800): 
		self.gpggaBAUDRATE = gpggaBaudrate
		self.gpggaComnum = gpggaComnum

		self.gpvtgBAUDRATE = gpvtgBaudrate 
		self.gpvtgComnum = gpvtgComnum 

	def initConnections(self): 

		#ser = serial.Serial()
		self.gpggaSerial = serialwin32.Serial()#serialwin32.Serial('/dev/tty.GarminGLO47d48-COM7')
		self.gpggaSerial.baudrate = self.gpggaBAUDRATE
		self.gpggaSerial.port = self.gpggaComnum
		self.gpggaSerial.timeout = 1
		self.gpggaSerial.open()
		self.gpggaSerial.isOpen() 
	
		print 'OPEN: '+ self.gpggaSerial.name
		print '' 


		self.gpvtgSerial = serialwin32.Serial()#serialwin32.Serial('/dev/tty.GarminGLO47d48-COM7')
		self.gpvtgSerial.baudrate = self.gpvtgBAUDRATE
		self.gpvtgSerial.port = self.gpvtgComnum
		self.gpvtgSerial.timeout = 1
		self.gpvtgSerial.open()
		self.gpvtgSerial.isOpen()  
	
		print 'OPEN: '+ self.gpvtgSerial.name
		print '' 


	def getLongLat(self):
		"""returns (longitude, latitude)"""
		try:    
			
			#line = self.gpggaSerial.readline()    
			#print ("\n      in newgpsdata calling readlastline") 
			#line = raw_input()
			#line = self.gpggaSerial.readlastline()   
			#print("\n      after line read.")    
			#line = raw_input()

			# print ("\n      in newgpsdata calling readline") 
			# raw_input()
			# line = self.gpggaSerial.readline()   
			# print("\n      after line read.")    
			# raw_input()

			lastLine = "0" 
			line = "0" 
			while line is not "" or (lastLine is "0" or lastLine is ""):
				print("lastLine was {0}".format(line))
				lastLine = line
				line = self.gpggaSerial.readline()   
			print("\n      after line read.")    
			#raw_input()

			line = lastLine

			print "   from gps: ", line  
			
			gpgga = nmea.GPGGA() 
			gpgga.parse(line)

			# example gpgga format line:
			#    $GPGGA,070010.5,4215.35012,N,07234.49672,W,2,15,0.7,85.1,M,-33.0,M,,*57
			#                    4215.35012,N,07234.49672,W
			#                    42 degrees N, -72 degrees W 

			lats = gpgga.latitude
			longs = gpgga.longitude 


			#print("  latitude: {0}\n  longitude: {1}".format(lats,longs))
			
			#convert degrees,decimal minutes to decimal degrees 
			lat1 = (float(lats[2]+lats[3]+lats[4]+lats[5]+lats[6]+lats[7]+lats[8]))/60
			lat = (float(lats[0]+lats[1])+lat1)
			long1 = (float(longs[3]+longs[4]+longs[5]+longs[6]+longs[7]+longs[8]+longs[9]))/60
			long = (float(longs[0]+longs[1]+longs[2])+long1)
			
			#calc position 
			pos_y = lat
			pos_x = -long #longitude is negative  

			#shows that we are reading through this loop
			print ("x: %f"  % pos_x)
			print ("y: %f"  % pos_y) 

			self.currentPosition = (pos_x,pos_y)

			return (pos_x,pos_y)

		except:
			print "error in stream_serial ", sys.exc_info()[0]
			pass 

	def getGroundSpeedAndBearing(self):
		try:    

			lastLine = "0" 
			line = "0" 
			while line is not "" or (lastLine is "0" or lastLine is ""):
				print("lastLine was {0}".format(line))
				lastLine = line
				line = self.gpvtgSerial.readline()   
			print("\n      after line read.")    
			#raw_input()

			line = lastLine

			print "   from gps: ", line  
			
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












