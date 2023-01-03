import os
import sys
import math
import time
import numpy as np
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt

R = 6371 #Earth's radius in km (approximate)
H = 415 #ISS orbital altitude in km (approximate)

#find lat and long using geopy
city = 'Fayetteville'
state = 'Arkansas'
country = 'US'

geolocator = Nominatim(user_agent = 'my_user_agent')
loc = geolocator.geocode(city + ',' + state + ',' + country)

lon1 = float(loc.longitude) #your current longitude
lat1 = float(loc.latitude) #your current latitude

#lon1=-94.581213
#lat1=39.099912


#ensures website opens silently
options=Options()
options.add_argument('--headless')
options.add_argument('log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])


#url of site containing ISS lat long
url = 'http://www.isstracker.com/'

#load the website using selenium, extract lat+long string
driver=webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
driver.get(url)


#set up plot
Rad = 1

x=[]
y=[]
circ_x=np.arange(-Rad,Rad,0.0001)
circ_y1=[np.sqrt(1-np.square(x))]
circ_y2=[-np.sqrt(1-np.square(x))]
color='red'

plt.ion()
plt.xlim(-Rad,Rad)
plt.ylim(-Rad,Rad)

graph = plt.plot(x,y,color=color)[0]

first_loop = True #ensures no plot wonkiness

try: 
    while True:
        
        long = driver.find_element(By.XPATH, '//*[@id="longitudeValue"]').text
        lat = driver.find_element(By.XPATH, '//*[@id="latitudeValue"]').text

        os.system('CLS')

        lon2 = float(long)
        lat2 = float(lat)

        #compute bearing
        
        lat1_rad=np.deg2rad(lat1)
        lat2_rad=np.deg2rad(lat2)
        lon1_rad=np.deg2rad(lon1)
        lon2_rad=np.deg2rad(lon2)

        del_lon=lon2_rad-lon1_rad
        del_lat=lat2_rad-lat1_rad

        X = (np.cos(lat2_rad))*(np.sin(del_lon))
        Y = ((np.cos(lat1_rad))*(np.sin(lat2_rad))) - ((np.sin(lat1_rad))*(np.cos(lat2_rad))*(np.cos(del_lon)))

        bearing = math.atan2(X,Y)
        bearing_deg = np.rad2deg(bearing)

        #if negative bearing (past due south), add 360 to flip back to positive
        if bearing_deg < 0:
            bearing_deg = 360 + bearing_deg
            bearing = (2*np.pi) + bearing

        print(f'Azimuth: {bearing_deg}')



        #compute elevation

        a = np.square(np.sin(del_lat/2)) + np.cos(lat1_rad)*np.cos(lat2_rad)*np.square(np.sin(del_lon/2))
        
        C = 2*math.atan2(np.sqrt(a),np.sqrt(1-a)) #angle between coordinates (in radians)

        c = np.sqrt(
                    np.square(R) + np.square(R+H) - (2*R*(R+H)*np.cos(C))
                    )

        delta = np.arccos(
                            (np.square(R) - np.square(c) - np.square(R+H))  /
                            (-2*c*(R+H))
                            )

        theta = np.pi - delta - C

        el = theta-(np.pi/2)

        el_deg = np.rad2deg(el)

        print(f'Elevation: {el_deg}')



        #generate plot point
        d = Rad*np.cos(el)

        if bearing_deg <= 90:
            x_coord = d*np.sin(bearing)
            y_coord = d*np.cos(bearing)

        elif 90 < bearing_deg <= 180:
            x_coord = d*np.cos(bearing-(np.pi/2))
            y_coord = -d*np.sin(bearing-(np.pi/2))

        elif 180 < bearing_deg <= 270:
            x_coord = -d*np.cos(((3*np.pi)/2) - bearing)
            y_coord = -d*np.sin(((3*np.pi)/2) - bearing)

        else:
            x_coord = -d*np.cos(bearing - ((3*np.pi)/2))
            y_coord = d*np.sin(bearing - ((3*np.pi)/2))


        #update plot
        if first_loop:
            first_loop = False
        else:
            x.append(x_coord)
            y.append(y_coord)

            if el_deg >= 0:
                color = 'blue'
            else:
                color = 'red'

            if len(x) > 100000: #ensure the list doesn't get unmanagably large.
                x.pop(0)
                y.pop(0)

            graph = plt.plot(x,y,color=color)[0]
            plt.draw()

        time.sleep(1)
        plt.pause(0.0001)
        
except KeyboardInterrupt:
    pass

driver.quit()
sys.exit()

