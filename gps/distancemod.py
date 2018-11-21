import MySQLdb
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians
import googlemaps 
  
# Requires API key 
gmaps = googlemaps.Client(key='AIzaSyA3V5dYN3y2TPb4VhvpyL9NnW2k86wKGG0') 
  
# approximate radius of earth in km
R = 6373.0
latv =52.2296756
lonv = 21.0122287
geolocator = Nominatim(user_agent="hi")
def find_distance(lat1,lat2,lon1,lon2):
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	return distance
	#print("Result:", distance)
	#print("Should be:", 278.546, "km")

def find_place(lat,lon):
	#geolocator = Nominatim(user_agent="specify_your_app_name_here")
	temp='"'+str(lat)+','+str(lon)+'"'
	print(temp)
	location = geolocator.reverse(temp)
	return location.address
	
	
	
db = MySQLdb.connect("localhost","phpmyadmin","jithesh@55","mp" )
i=1
# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
while (i==1):
	cur.execute("SELECT * FROM location WHERE active=1")
 	i=2
    
	for row in cur.fetchall() :
		#data fetching
    		lata=row[1]
    		lona=row[2]
    		latd=row[4]
    		lond=row[5]
    		#reversing lattitude to place
    		reversea=find_place(lata,lona)
    		reversev=find_place(latv,lonv)
    		reversede=find_place(latd,lond)
    		#print(reversede)
    		#find distance
    		distancevd=find_distance(latv,latd,lonv,lond)
    		distancead=find_distance(lata,latd,lona,lond)
    		if(distancead>=distancevd):
   			print "lattitudeambulance:",row[1],"  logitudeambulance:",row[2]
    			distanceva=find_distance(latv,lata,lonv,lona)
    		
    			#print("Distance between them:", distance,"km")
    			if(distanceva<0.1):
    				print("Alert nearby 100m")
    			elif(distanceva<0.25):
    				print("Alert nearby 250m")
    			elif(distanceva<0.5):
    				print("Alert nearby 500m")
    			elif(distanceva<0.75):
    				print("Alert nearby 750m")
    			elif(distanceva<1):
    				print("Alert nearby 1km")
    			elif(distanceva<2):
    				print("Alert nearby 2km")
