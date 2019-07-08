#!/usr/bin/env python
#
# This is a python script for importing brightness data from LightShow Pi to use to send CAN messages

from __future__ import print_function
import can
import subprocess
from array import array
import sys

"""
result = (([max value of range in init] - [min value of range in int]) * ([input value in int] - [min value of byte, so 0])) / (]max value of byte range so 255] - [min value of bytre range so 0]) + [min value of range in init]
"""


def carData(dataArray): 
	# Time to have some fun - what to do for the car
	# Here we have 8 channels to play with, where the range in each channel is 0.0 to 1.0 (as it gets clipped previously)
	
	#Create a new array to hold the CAN data values
	canvalues = array('i')
	#Now convert the value into something we can use in the car, which ranges from 0 to 255
	for numConvert in range(0, len(dataArray)):
		intValue = int(round(float((dataArray[numConvert] * 255))))
		canvalues.insert(numConvert, intValue)
		
		
	#Display the Frequency coming in and it's value - Debugging
	#for arrayNumber in range(0, len(canvalues)):
        #    #sys.stdout.write(arrayNumber)
        #    #sys.stdout.write("\t\t")
        #    #sys.stdout.write("\r\n")
	#    sys.stdout.write(str(canvalues[arrayNumber]))
        #    sys.stdout.write("\t\t")
        #sys.stdout.write("\r\n")
		

	#########################################################
	#	Each channel corrisponds to a frequency, so we will label there here
	#
	#	Bass tones tend to sit somewhere between the three bass levels
	#	Vocals tend to sit somewhere in the mid tones
	#	High Tones tend to be high vocals or symbols
	#########################################################
	LowBass = 0
	MidBass = 1
	HighBass = 2
	LowMidTones = 3
	MidMidTones = 4
	HighMidTones = 5
	LowHighTones = 6
	HighHighTones = 7	
	
	#########################################################
	#	This is where we define which channel gets mapped to which 'thing' in the cluster
	#########################################################
	
	
	#Speedo isn't reactive so this is mapped to low tones
	#Speedo and RPM
	can_message(speedo_and_rpm().getID(), speedo_and_rpm().getData(canvalues[LowBass]))
	
	#Engine temp isn't reactive so we map to low tones
	#Engine Temp
	can_message(enginetemp().getID(), enginetemp().getData(canvalues[LowBass]))	
	
	#Engine temp isn't reactive so we map to low tones
	#Fuel Guage
	can_message(fuel().getID(), fuel().getData(canvalues[LowBass]))
	
	#Left hand LEDs
	can_message(left_side_leds().getID(), left_side_leds().getData(canvalues[MidBass]))
	
	#Right Side LEDS
        can_message(right_side_leds().getID(), right_side_leds().getData(canvalues[HighBass]))
	
	#Trip Recorder
        can_message(trip_recorder().getID(), trip_recorder().getData(canvalues[HighHighTones]))
	
	#Milage - Removed for now as it breaks the display
        #can_message(milage().getID(), milage().getData(canvalues[HighHighTones]))
	
	
	
	#Brightness
	#can_message(brightness().getID(), brightness().getData(canvalues[MidBass]))

	

	



	


def can_message(id, bytedata):
    can_interface = 'can0'
    bus = can.interface.Bus(can_interface, bustype='socketcan_native')
    #bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)
    #bus = can.interface.Bus(bustype='ixxat', channel=0, bitrate=250000)
    #bus = can.interface.Bus(bustype='vector', app_name='CANalyzer', channel=0, bitrate=250000)
	
    sys.stdout.write("Channel ")
    sys.stdout.write(str(id))
    sys.stdout.write("\t\tData ")
    sys.stdout.write(str((bytedata)))
    sys.stdout.write("\r\n")

    msg = can.Message(arbitration_id=id,
                      data=bytedata,
                      extended_id=False)
    try:
        bus.send(msg)
        #print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")
		
		
class brightness:
	def getID(self):
		return int('036', 16)

	def getData(self, value):
		# Brightness range are 7 values for each type, so we have 14 values to play with. 
		# 256 / 14 = 18...with a bit left
		
		#Brightness is set on byte 4, so we build a string based on that
		byte0 = 0x00
		byte1 = 0x00
		byte2 = 0x00
		byte3 = 0x00
		byte4 = 0x00
		byte5 = 0x00
		byte6 = 0x00
		byte7 = 0x00
		data = 00
		
		""""	

	All areas but fuel off
		32 	min
		34	nearly min
		36	nearly default
		38	default brightness
		3a	Brighter
		3c	Brighter still
		3e	max brightness
		"""
		
		if (value <=18):
			data = 0x22				#Min Brightness all areas
		elif (value <=36):
			data = 0x24				#Nearly Min Brightness all areas
		elif (value <=54):
			data = 0x26				#Nearly Default all areas
		elif (value <=72):
			data = 0x28				#Default brightness all areas
		elif (value <=90):
			data = 0x2a				#Slightly brighter than default all areas
		elif (value <=108):
			data = 0x2c				#Brighter still all areas	
		elif (value <=126):
			data = 0x2e				#Max brightness all areas			
		elif (value <=144):
			data = 0x32				#Min Brightness all areas not fuel
		elif (value <=162):
			data = 0x34				#Nearly Min Brightness all areas not fuel
		elif (value <=180):
			data = 0x36				#Nearly Default all areas not fuel
		elif (value <=196):
			data = 0x38				#Default brightness all areas not fuel
		elif (value <=216):
			data = 0x3a				#Slightly brighter than default all areas not fuel
		elif (value <=234):
			data = 0x3c				#Brighter still all areas not fuel
		elif (value <=255):
			data = 0x3e				#Max brightness all areas not fuel

		
		#data = '0x' + data
		bytedata = [byte0, byte1, byte2, data, byte4, byte5, byte6, byte7]
		return bytedata
		
		
class fuel:
	def getID(self):
		return int('161', 16)

	def getData(self, value):
		
		#Fuel is set on byte 4, so we build a string based on that
		byte0 = 0x00
		byte1 = 0x00
		byte2 = 0x00
		byte3 = 0x00
		byte4 = 0x00
		byte5 = 0x00
		byte6 = 0x00
		byte7 = 0x00
		data = 00
		
		""""	
		00		Nothing in the tank
		19		1/4 tank
		32		Half tank
		4B		3/4 tank
		64		Max tank
		"""
		
		if (value <=52):
			data = 0x00				#Nothing in the tank
		elif (value <=104):
			data = 0x19				#1/4 in the tank
		elif (value <=156):
			data = 0x32				#Half tank
		elif (value <=208):
			data = 0x4B				#3/4 tank
		elif (value <=256):
			data = 0x64				#Full tank
			
		#data = '0x' + data
		bytedata = [byte0, byte1, byte2, data, byte4, byte5, byte6, byte7]
		return bytedata
		
		
class speedo_and_rpm:
	def getID(self):
		return int('0B6', 16)

	def getData(self, value):
		byte0 = 0x00
		byte1 = 0x00
		byte2 = 0x00
		byte3 = 0x00
		byte4 = 0x00
		byte5 = 0x00
		byte6 = 0x00
		byte7 = 0x00
		speedo = 00
		rpm = 00
		
		""""	
##############################
	ID 0B6
##############################

This seems to control speedo and RPM


Byte 1 - Controls RPM

	NEEDS MORE MAPPING OUT

	00 - 0rpm
	08 - 250 rpm
	10 - 500 rpm
	32 - 1.5k rpm
	64 - 3.25rpm
	96 - 4.75rpm
	a1 - Just over 5K rpm
	b0 - Just over 5.5k rpm
	cc - 6.5k
	dd (or around) - 7k

Byte 3 - Contols speedo

	This is actually pretty stupid. The speedo doesn't go up in consistant units, sometimes it's in 2s, sometimes it's in 1s. So you can't always get an exact speed

	00 - 0mph
	05 - 9mph
	12 - 31mph
	18 - 40mph
	1e - 50mph
	25 - 61pmh	
	2b - 70mph
	31 - 80mph
	38 - 91mph
	4a - 120 mph
	62 - 158 mph (max)
	"""
		
		if (value <=36):
			rpm = 0x00				
			speedo = 0x00
		elif (value <=54):
			rpm = 0x08
			speedo = 0x05
		elif (value <=72):
			rpm = 0x10
			speedo = 0x12
		elif (value <=90):
			rpm = 0x32
			speedo = 0x18
		elif (value <=108):
			rpm = 0x64
			speedo = 0x1e
		elif (value <=126):
			rpm = 0x96
			speedo = 0x25		
		elif (value <=144):
			rpm = 0xa1
			speedo = 0x2b
		elif (value <=162):
			rpm = 0xb0
			speedo = 0x31
		elif (value <=180):
			rpm = 0xc1
			speedo = 0x38
		elif (value <=196):
			rpm = 0xcc
			speedo = 0x4a
		elif (value <=255):
			rpm = 0xdd
			speedo = 0x62

		
		#data = '0x' + data
		bytedata = [rpm, byte1, speedo, byte3, byte4, byte5, byte6, byte7]
		return bytedata

			
class left_side_leds:
	def getID(self):
		return int('128', 16)

	def getData(self, value):
		
		#LEDs are on byte 1
		byte0 = 0x00
		byte1 = 0x00
		byte2 = 0x00
		byte3 = 0x00
		byte4 = 0x00
		byte5 = 0x00
		byte6 = 0x00
		byte7 = 0x00
		data = 00
		
		#Do our calculation to make things happen. As we have the full range the calculation becomes very easy
		#The range here is 00 to FF
		data = value
		
		bytedata = [data, byte1, byte2, byte3, byte4, byte5, byte6, byte7]
		return bytedata
	
class right_side_leds:
	def getID(self):
		return int('128', 16)

	def getData(self, value):
		
		#LEDs are on byte 8
		byte0 = 0x00
		byte1 = 0x00
		byte2 = 0x00
		byte3 = 0x00
		byte4 = 0x00
		byte5 = 0x00
		byte6 = 0x00
		byte7 = 0x00
		data = 0x00
		
		#Do our calculation to make things happen. We will use the full range for ease of use
		#The range here is 00 to FF
		data = value
		
		bytedata = [byte0, byte1, byte2, byte3, byte4, byte5, byte6, data]
		return bytedata
	
class trip_recorder:
	def getID(self):
		return int('1A8', 16)

	def getData(self, value):
		
		#LEDs are on bytes 6, 7 and 8
		byte0 = 0x00
		byte1 = 0x00
		byte2 = 0x00
		byte3 = 0x00
		byte4 = 0x00
		byte5 = 0x00
		byte6 = 0x00
		byte7 = 0x00
		data = 0x00
		
		#Do our calculation to make things happen. 
		#We have 3 separate bytes to play with here, but to make life easy we'll set all 3 the same
		smalltrip = 0
		midtrip = 0
		hightrip = 0
		
                if (value <=85):
		    smalltrip = value
                    midtrip = 0
                    hightrip = 0
                elif (value <=160):
		    smalltrip = value
                    midtrip = value
                    hightrip = 0
                elif (value <=255):
		    smalltrip = value
                    midtrip = value
                    hightrip = value
		
		bytedata = [byte0, byte1, byte2, byte3, byte4, smalltrip, midtrip, hightrip]
		return bytedata
	
class milage:
	def getID(self):
		return int('0F6', 16)

	def getData(self, value):
		
		#LEDs are on bytes 3, 4 and 5
		byte0 = 0x00
		byte1 = 0x00
		byte2 = 0x00
		byte3 = 0x00
		byte4 = 0x00
		byte5 = 0x00
		byte6 = 0x00
		byte7 = 0x00
		data = 0x00
		
		#Do our calculation to make things happen. 
		#We have 3 separate bytes to play with here, but to make life easy we'll set all 3 the same
		smalltrip = 0
		midtrip = 0
		hightrip = 0
		
                if (value <=85):
		    smalltrip = value
                    midtrip = 0
                    hightrip = 0
                elif (value <=160):
		    smalltrip = value
                    midtrip = value
                    hightrip = 0
                elif (value <=255):
		    smalltrip = value
                    midtrip = value
                    hightrip = value
		
		bytedata = [byte0, byte1, smalltrip, midtrip, hightrip, byte5, byte6, byte7]
		return bytedata
		
		

class enginetemp:
	def getID(self):
		return int('0F6', 16)
		
	def getData(self, value):
		
		#Temps are on byte 2 but Byte1 needs to be FF 
		byte0 = 0xFF
		byte1 = 0x00
		byte2 = 0x00
		byte3 = 0x00
		byte4 = 0x00
		byte5 = 0x00
		byte6 = 0x00
		byte7 = 0x00
		data = 00
		
		#Do our calculation to make things happen. 
		#The range here is 5A to A0
		data = ((50) * (value - 90)) / (50) + 90
		
		bytedata = [byte0, data, byte2, byte3, byte4, byte5, byte6, byte7]
		return bytedata
	
			
			
			
			
			
			
			
			
