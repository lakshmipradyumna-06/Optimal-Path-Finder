from geopy.geocoders import Nominatim
import pandas as pd
import pickle

print('This is the python Code to get the latitude and longitude of places listed in list of places')

df=pd.DataFrame(columns=['location','latitude','longitude'])

geolocator = Nominatim(user_agent="my-application",timeout=10)

file = open("a.txt", "r")
file1 = open("b.txt", "w")

line = file.readlines()

t = 0
notfound = []
''''
Reading line by line and storing the latitude and longitude of the listed places
'''
for i in line:
	try:
		print (str(i))
		x = str(i).rstrip('\n')
		location = geolocator.geocode(x)
		df.loc[t] = [x, location.latitude, location.longitude]
		t = t+1
	except:
		notfound.append(x)

print ("Locations")
#print (df)

print ('Downloading Cordinated CSV file named:cordinates.csv')
df.to_csv('cordinates.csv')


with open("b.txt","wb") as fp:
	pickle.dump(notfound,fp)
