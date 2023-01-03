import time
import os
import sys
from geopy.geocoders import Nominatim
import numpy as np
import datetime
from datetime import datetime



#find lat and long using geopy
city = 'Fayetteville'
state = 'Arkansas'
country = 'US'

geolocator = Nominatim(user_agent = 'my_user_agent')
loc = geolocator.geocode(city + ',' + state + ',' + country)

long = loc.longitude #your current longitude
lat = loc.latitude #your current latitude



try:
    while True:

        os.system('cls')
        
        #scrape ISS RA and DEC from statflare: Yet to solve
        
        
        #for testing: Andromeda Galaxy
        # RA and DE coordinates are effectively fixed for deep sky objects. Input those coordinates here
        # Enter coordinates in decimal deg
        RA = 10.6833 # right accension of object
        DE = 41.2692 # declination of object

        J2000 = datetime(2000,1,1,12)
        curDate = datetime.utcnow()

        J2000_delta = curDate-J2000 #compute time since J2000 epoch

        J2000_delta = J2000_delta.days + (J2000_delta.seconds/(60*60*24)) #convert to decimal days

        dec_UTC = curDate.hour + (curDate.minute/60) + (curDate.second/3600) #decimal UTC (from hh:mm:ss)

        LST = (100.46 + 0.985647*J2000_delta + long + 15*dec_UTC)%360 #compute local siderial time

        HA = LST - RA #compute hour angle

        #compute alt and az

        ALT = np.degrees(np.arcsin((np.sin(np.deg2rad(DE))*np.sin(np.deg2rad(lat))) +
                                   (np.cos(np.deg2rad(DE))*np.cos(np.deg2rad(lat))*np.cos(np.deg2rad(HA)))))

        AZ = np.degrees(np.arccos((np.sin(np.deg2rad(DE)) - (np.sin(np.deg2rad(ALT))*np.sin(np.deg2rad(lat)))) /
                        (np.cos(np.deg2rad(ALT))*np.cos(np.deg2rad(lat)))))

        if np.sin(np.deg2rad(HA)) > 0: #flip azimuth if necessary
            AZ = 360 - AZ

        print('OBJECT: ANDROMEDA GALAXY')
        print(' ')
        print('CURRENT POSITION: ')
        print(f'ALT: {ALT}')
        print(f'AZ: {AZ}')
        print(' ')

        time.sleep(1)
        
except KeyboardInterrupt:
    sys.exit() #close terminal


