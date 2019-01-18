import MySQLdb
from geopy.geocoders import Nominatim
import math
from math import radians, sin, cos, acos
import googlemaps 
gmaps = googlemaps.Client(key='XXXXXXXXXXXXXXXXXXXXXXX') 
latv =10.038832
lonv = 76.613547
geolocator = Nominatim(user_agent="specify_your_app_name_here")

def calculate_initial_compass_bearing(lata,lona,latb,lonb):
    startx,starty,endx,endy=lata,lona,latb,lonb
    angle=math.atan2(endy-starty, endx-startx)
    if angle>=0:
        return math.degrees(angle)
    else:
        return math.degrees((angle+2*math.pi))
        

def find_distance(reversef,reverset,lata,lona,latd,lond):
	temp1="'"+reversef+'"'
	temp2="'"+reverset+'"'
	my_dist = gmaps.distance_matrix(temp1,temp2)['rows'][0]['elements'][0]
	#my_dist = gmaps.distance_matrix(reversef,reverset)['rows'][0]['elements'][0]
	distance=my_dist["distance"]["value"]
	#print(distance)
	#distance=100
	distance=distance/1.0
	return distance
	
def actual_distance(lata,lona,latd,lond):
	#print("hi")
	slat=radians(lata)
	slon=radians(lona)
	elat=radians(latd)
	elon=radians(lond)
	distance=6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
	distance=distance*1000
	return distance
	#print('distanxce')
	#print (distance)
	
	
	
def find_place(lat,lon):
	temp=str(lat)+','+str(lon)
	print(temp)
	location = geolocator.reverse(temp)

	return location.address
	
	
	
#db = MySQLdb.connect("localhost","phpmyadmin","jithesh@55","mp" )
db = MySQLdb.connect("remotemysql.com","uZanCOgf53","HxYE8xG7vl","uZanCOgf53" )
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
    		print("ambulance:",reversea)
    		reversev=find_place(latv,lonv)
    		print("vehicle:",reversev)
    		reversede=find_place(latd,lond)
    		print("destination:",reversede)
    		#print(reversede)
    		#print("hi")
    		#find distance
    		distancead=find_distance(reversea,reversede,lata,lona,latd,lond)
    		print("amb-dest:")
    		print distancead
    		distancevd=find_distance(reversev,reversede,latv,lonv,latv,lonv)
    		print("des-veh:")
    		print distancevd
    		distanceav=find_distance(reversea,reversev,latv,lonv,latd,lond)
    		print("amb-veh:")
    		print distanceav
    		distancetest=distancevd+distanceav-15
    		print("test:")
    		print distancetest
    		if(distancetest<=distancead):
    			if(distancead>=distancevd):
   				
    				distanceva=find_distance(reversev,reversea,latv,lonv,lata,lona)
    				print("in path")
    				distanceva=actual_distance(latv,lonv,lata,lona)
    				distancead=actual_distance(lata,lona,latd,lond)
    				distancevd=actual_distance(latv,lonv,latd,lond)
    				if((distanceva<100)and(distancevd<distancead)):
    					print("Alert nearby 100m")
    					
    					angle=calculate_initial_compass_bearing(latv,lonv,lata,lona)
					print("Angle:")
					print angle
					if(angle<20):
						print("Ambulance approaching from North direction");
					elif(angle<70):
						print("Ambulance approaching from North-East direction"); 
					elif(angle<110):
						print("Ambulance approaching from East direction"); 
					elif(angle<160):
						print("Ambulance approaching from South-East direction"); 
					elif(angle<200):
						print("Ambulance approaching from South direction"); 
					elif(angle<250):
						print("Ambulance approaching from South-West direction"); 
					elif(angle<290):
						print("Ambulance approaching from West direction"); 
					elif(angle<340):
						print("Ambulance approaching from North-West direction"); 
					elif(angle<=360):
						print("Ambulance approaching from North direction"); 

    				elif((distanceva<250)and(distancevd<distancead)):
    					
    					print("Alert nearby 250m")
    					
    					angle=calculate_initial_compass_bearing(latv,lonv,lata,lona)
					print("Angle:")
					print angle
					if(angle<20):
						print("Ambulance approaching from North direction");
					elif(angle<70):
						print("Ambulance approaching from North-East direction"); 
					elif(angle<110):
						print("Ambulance approaching from East direction"); 
					elif(angle<160):
						print("Ambulance approaching from South-East direction"); 
					elif(angle<200):
						print("Ambulance approaching from South direction"); 
					elif(angle<250):
						print("Ambulance approaching from South-West direction"); 
					elif(angle<290):
						print("Ambulance approaching from West direction"); 
					elif(angle<340):
						print("Ambulance approaching from North-West direction"); 
					elif(angle<=360):
						print("Ambulance approaching from North direction"); 
    				elif((distanceva<500)and(distancevd<distancead)):
    					
    					print("Alert nearby 500m")
    					
    					angle=calculate_initial_compass_bearing(latv,lonv,lata,lona)
					print("Angle:")
					print angle
					if(angle<20):
						print("Ambulance approaching from North direction");
					elif(angle<70):
						print("Ambulance approaching from North-East direction"); 
					elif(angle<110):
						print("Ambulance approaching from East direction"); 
					elif(angle<160):
						print("Ambulance approaching from South-East direction"); 
					elif(angle<200):
						print("Ambulance approaching from South direction"); 
					elif(angle<250):
						print("Ambulance approaching from South-West direction"); 
					elif(angle<290):
						print("Ambulance approaching from West direction"); 
					elif(angle<340):
						print("Ambulance approaching from North-West direction"); 
					elif(angle<=360):
						print("Ambulance approaching from North direction"); 
    				elif((distanceva<750)and(distancevd<distancead)):
    					
    					print("Alert nearby 750m")
    					
    					angle=calculate_initial_compass_bearing(latv,lonv,lata,lona)
					print("Angle:")
					print angle
					if(angle<20):
						print("Ambulance approaching from North direction");
					elif(angle<70):
						print("Ambulance approaching from North-East direction"); 
					elif(angle<110):
						print("Ambulance approaching from East direction"); 
					elif(angle<160):
						print("Ambulance approaching from South-East direction"); 
					elif(angle<200):
						print("Ambulance approaching from South direction"); 
					elif(angle<250):
						print("Ambulance approaching from South-West direction"); 
					elif(angle<290):
						print("Ambulance approaching from West direction"); 
					elif(angle<340):
						print("Ambulance approaching from North-West direction"); 
					elif(angle<=360):
						print("Ambulance approaching from North direction"); 
    				elif((distanceva<1000)and(distancevd<distancead)):
    					print("Alert nearby 1 km")
    					
    					angle=calculate_initial_compass_bearing(latv,lonv,lata,lona)
					print("Angle:")
					print angle
					if(angle<20):
						print("Ambulance approaching from North direction");
					elif(angle<70):
						print("Ambulance approaching from North-East direction"); 
					elif(angle<110):
						print("Ambulance approaching from East direction"); 
					elif(angle<160):
						print("Ambulance approaching from South-East direction"); 
					elif(angle<200):
						print("Ambulance approaching from South direction"); 
					elif(angle<250):
						print("Ambulance approaching from South-West direction"); 
					elif(angle<290):
						print("Ambulance approaching from West direction"); 
					elif(angle<340):
						print("Ambulance approaching from North-West direction"); 
					elif(angle<=360):
						print("Ambulance approaching from North direction"); 
    			
    			else:
    				distanceva=find_distance(reversev,reversea)
    				print("in opp path")
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
    		else:
    			print("NOT IN ROUTE")
