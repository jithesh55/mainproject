import MySQLdb
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians
import googlemaps 
  
# Requires API key 
gmaps = googlemaps.Client(key='AIzaSyAdeQLzsHBCh2AzcrXv5noaYLWtuyJMbSw') 
  
# approximate radius of earth in km
R = 6373.0
latv =10.114700
lonv = 76.477798
geolocator = Nominatim(user_agent="jithesh")


def find_distance(reversef,reverset):
	my_dist = gmaps.distance_matrix(reversef,reverset)['rows'][0]['elements'][0]
	distance=my_dist["distance"]["value"]
	distance=distance/1000.0
	print (distance)
	return distance
	
	
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
while (True):
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
    		print("ambulance:",reversea)
    		reversev=find_place(latv,lonv)
    		print("vehicle:",reversev)
    		reversede=find_place(latd,lond)
    		print("destination:",reversede)
    		print(reversede)
    		
    		#find distance
    		distancevd=find_distance(reversev,reversede)
    		distancead=find_distance(reversea,reversede)
    		if(distancead>=distancevd):
   			#print "lattitudeambulance:",row[1],"  logitudeambulance:",row[2]
    			distanceva=find_distance(reversev,reversea)
    		
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
    		else:
    			distanceva=find_distance(reversev,reversea)
    		
    			#print("Distance between them:", distance,"km")
    			if(distanceva<0.1):
    				print("OPPOSITE Alert nearby 100m")
    			elif(distanceva<0.25):
    				print("OPPOSITE Alert nearby 250m")
    			elif(distanceva<0.5):
    				print("OPPOSITE Alert nearby 500m")
    			elif(distanceva<0.75):
    				print("OPPOSITE Alert nearby 750m")
    			elif(distanceva<1):
    				print("OPPOSITE Alert nearby 1km")
    			elif(distanceva<2):
    				print("OPPOSITE Alert nearby 2km")
