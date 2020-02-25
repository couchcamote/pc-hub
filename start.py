#!/usr/bin/python3

import gpsd


def init_services():
	print('Initializing Services ... ')
	gpsd.connect()

def get_gps_data():
	packet = gpsd.get_current()
	return packet


if __name__ == "__main__":

	print('Starting PC Hub - Transportation Payment Application ... ')

	init_services()

	gpspacket = get_gps_data()

	lon = gpspacket.lon
	lat = gpspacket.lat
	time = gpspacket.time

	print ('Print ....')

	print('Longitude: '+ str(lon)+', Latitude: '+str(lat))
	print('UTC Time: '+ str(time))


