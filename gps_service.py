#!/usr/bin/python3

import gpsd


def init_service():
	print('Initializing Services ... ')
	gpsd.connect()

def get_gps_data():
	packet = gpsd.get_current()
	return packet

def print_gps_data():
	print('Print GPS Data... ')
	packet = gpsd.get_current()

	if not packet:
		print('Try to connect')
		init_service()
		packet = gpsd.get_current()
		lon = packet.lon
		lat = packet.lat
		time = packet.time
		print('Time : '+str(time)+  ' Longitude: '+ str(lon)+', Latitude: '+str(lat))

	packet = gpsd.get_current()
	lon = packet.lon
	lat = packet.lat
	time = packet.time
	print('Time : '+str(time)+  ' Longitude: '+ str(lon)+', Latitude: '+str(lat))

if __name__ == "__main__":

	print('Initializing GPS Service ... ')

	init_service()

	gpspacket = get_gps_data()

	lon = gpspacket.lon
	lat = gpspacket.lat
	time = gpspacket.time

	print ('Print ....')

	print('Longitude: '+ str(lon)+', Latitude: '+str(lat))
	print('UTC Time: '+ str(time))


