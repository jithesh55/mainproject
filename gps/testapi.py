
# importing googlemaps module 
import googlemaps 
  
# Requires API key 
gmaps = googlemaps.Client(key='AIzaSyAdeQLzsHBCh2AzcrXv5noaYLWtuyJMbSw') 
  
# Requires cities name 
my_dist = gmaps.distance_matrix('Delhi','Mumbai')['rows'][0]['elements'][0] 
print(my_dist) 
dist=my_dist["distance"]["value"]
# Printing the result 
print(dist) 

