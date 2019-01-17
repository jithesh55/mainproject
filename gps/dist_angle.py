import MySQLdb
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians
import googlemaps 
  
# Requires API key 
gmaps = googlemaps.Client(key='AIzaSyCAKlU5X7XNVJxEoLBL8kTm7gozhbr7jMI') 
  
# approximate radius of earth in km
R = 6373.0
latv =10.0575077
lonv = 76.61581430000001
geolocator = Nominatim(user_agent="jithesh")


def find_distance(reversef,reverset):
	my_dist = gmaps.distance_matrix(reversef,reverset)['rows'][0]['elements'][0]
	distance=my_dist["distance"]["value"]
	distance=distance/100.0
	#print (distance)
	return distance
	
	
def find_place(lat,lon):
	#geolocator = Nominatim(user_agent="specify_your_app_name_here")
	temp='"'+str(lat)+','+str(lon)+'"'
	print(temp)
	location = geolocator.reverse(temp)
	return location.address
	
	
	
db = MySQLdb.connect("localhost","phpmyadmin","jithesh@55","mp" )
i=1
k=1
print(coordinates('paris'))
# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
while (k==0):
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
    		print("amb-dist:")
    		print distancead
    		print("des-veh:")
    		print distancevd
    		if(distancead>=distancevd):
   			#print "lattitudeambulance:",row[1],"  logitudeambulance:",row[2]
    			distanceva=find_distance(reversev,reversea)
    		
    			#print("Distance between them:", distance,"km")
    			if(distanceva<100):
    				print("Alert nearby 100m")
    			elif(distanceva<250):
    				print("Alert nearby 250m")
    			elif(distanceva<500):
    				print("Alert nearby 500m")
    			elif(distanceva<750):
    				print("Alert nearby 750m")
    			elif(distanceva<1000):
    				print("Alert nearby 1km")
    			
    		else:
    			distanceva=find_distance(reversev,reversea)
    		
    			#print("Distance between them:", distance,"km")
    			if(distanceva<100):
    				print("OPPOSITE Alert nearby 100m")
    			elif(distanceva<250):
    				print("OPPOSITE Alert nearby 250m")
    			elif(distanceva<500):
    				print("OPPOSITE Alert nearby 500m")
    			elif(distanceva<750):
    				print("OPPOSITE Alert nearby 750m")
    			elif(distanceva<1000):
    				print("OPPOSITE Alert nearby 1km")
    			
