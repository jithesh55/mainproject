import MySQLdb
from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0
lat1 = radians(52.2296756)
lon1 = radians(21.0122287)
def find_distance(lat1,lat2,lon1,lon2):
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	return distance
	#print("Result:", distance)
	#print("Should be:", 278.546, "km")


db = MySQLdb.connect("localhost","phpmyadmin","jithesh@55","mp" )
 
# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
while (True):
	cur.execute("SELECT * FROM location WHERE active=1")
 
# print the first and second columns      
	for row in cur.fetchall() :
    		lat2=radians(row[1])
    		lon2=radians(row[2])
   		print "lattitude1:",row[1],"  logitude1:",row[2]
    		distance=find_distance(lat1,lat2,lon1,lon2)
    		print("Distance between them:", distance,"km")
    		if(distance<0.1):
    			print("Alert nearby 100m")
    		elif(distance<0.25):
    			print("Alert nearby 250m")
    		elif(distance<0.5):
    			print("Alert nearby 500m")
    		elif(distance<0.75):
    			print("Alert nearby 750m")
    		elif(distance<1):
    			print("Alert nearby 1km")
    		elif(distance<2):
    			print("Alert nearby 2km")
