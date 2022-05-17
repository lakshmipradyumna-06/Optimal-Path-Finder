import pickle
from heapq import heappush,heappop
import pandas as pd
import gmplot
import numpy as np
import requests
import json
import re
print('Importing Libraries.............')



print ('Loading Adjancency Matrix......')
with open('adj_mat.pkl','rb') as fp:
 	a=pickle.load(fp)

df = pd.read_csv('cordinates.csv') #Reading LATITUDE AND LONGITUDE DATASET CSV File()
open1=[]# Priority Queue ::Queue of pair of Nodeid and their correspoding score accoring to A* Algorithm
open2=[]
closed=[]# List of pair of Nodeid and their correspoding score accoring to A* Algorithm
#f = g+h

''''
Starting Destination :
start_dest
'''
start_dest=40
''''
Ending Destination :
end_dest
'''
end_dest=39

len_listofplaces=len(a)

def compdis(loc1,loc2):
	'''
	Function to calculate the HEURISTIC DISTANCE between loc1,loc2

	Parameters:-
	loc1(int): Node_id of 1st Location
	loc2(int): Node_id of 1st Location

	Returns
	Distance(float): Fetched from Bing Maps API
	'''

	lat_i = df.iloc[loc1]['latitude']
	long_i = df.iloc[loc1]['longitude']

	lat_j = df.iloc[loc2]['latitude']
	long_j = df.iloc[loc2]['longitude']

	lon_i  = long_i.tolist()
	lon_j = long_j.tolist()

	lati = lat_i.tolist()
	latj = lat_j.tolist()

	key = 'Aq8LlcKLQyS0vyUEhI7Zg-KXeH7SZeJ9o8vJtrZ92_fi_NCcS3W8FY_jgh53RdaI'
	print( "Sending request to bing maps API" )
	URL = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins='
	URL = URL + str( lat_i ) + ',' + str( long_i ) + '&destinations=' + str( lat_j ) + ',' + str(
		lon_j ) + '&travelMode=driving&timeUnit=seconds' + '&key=' + key
	data = requests.get( URL ).text
	json_data = json.loads( data )
	obj = json_data['resourceSets'][0]['resources'][0]['results'][0]
	return int(obj['travelDistance'])

def trace_path(closed,start_dest,end_dest):
	'''
	Function to trace final path from start_dest and start_dest

	Parameters:-
	closed(List): Closed list consist of of all the considered nodes while running A* Algorithms
	start_dest(int): Node_id of Starting Location
	start_dest(int): Node_id of Ending Location

	Returns
	Path(list) : Series of Nodeid representing the Solution Path
	lat(list)  : Series of Latitudes representing the Solution Path
	lon(list)  : Series of Longitudes representing the Solution Path
	'''
	print (closed[len(closed)-1])
	lat = []
	lon = []
	prev = end_dest
	lat.append(df.iloc[end_dest]['latitude'])
	lon.append(df.iloc[end_dest]['longitude'])
	path = []
	path.append(end_dest)
	while len(closed)>0:
		l = len(closed)
		curr , temp = closed[l-1]
		if curr == start_dest:
			path.append(curr)
			lat.append(df.iloc[curr]['latitude'])
			lon.append(df.iloc[curr]['longitude'])
			break
		#print (prev,curr)
		if a[prev][curr]>0:
			if l >=2:
				prev2,temp2 = closed[l-2]
				if a[prev2][curr] < a[prev][prev2]:
					closed.remove((curr,temp))
					continue


			path.append(curr)
			lat.append(df.iloc[curr]['latitude'])
			lon.append(df.iloc[curr]['longitude'])
			prev = curr
			closed.remove((curr,temp))

		else:
			closed.remove((curr,temp))
	return path,lat,lon

def timefunc(y,i):
	'''
	Function to calculate time to reach from y to i using Google Metrics API

	Parameters:-
	y(int): Node_id of Starting Location
	i(int): Node_id of Ending Location

	Returns
	Time(int) : Time taken to rreach from y to i in minutes
	'''
	start_dest=y
	end_dest=i
	start_lat = df.iloc[start_dest]['latitude']
	start_lon = df.iloc[start_dest]['longitude']

	end_lat = df.iloc[end_dest]['latitude']
	end_lon = df.iloc[end_dest]['longitude']

	key = 'Aq8LlcKLQyS0vyUEhI7Zg-KXeH7SZeJ9o8vJtrZ92_fi_NCcS3W8FY_jgh53RdaI'
	print("Sending request to bing maps API")
	URL = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins='
	URL = URL + str(start_lat) + ',' + str(start_lon) + '&destinations=' + str(end_lat) + ',' + str(end_lon) + '&travelMode=driving&timeUnit=seconds' + '&key=' + key
	data = requests.get(URL).text
	json_data = json.loads(data)
	obj = json_data['resourceSets'][0]['resources'][0]['results'][0]
	#obj = json_data['rows'][0]['elements'][0]
	print('distance', obj['travelDistance'])
	print('time', obj['travelDuration'])
	#print ((int(re.search(r'\d+', obj['duration']['text']).group())))
	#int(re.search(r'\d+', string1).group())
	return (int(re.search(r'\d+', str(obj['travelDuration'])).group()))


'''
Adding the current path
'''''
open1.append((compdis(start_dest,end_dest),start_dest))
g = np.zeros(len(a),dtype = np.float64)
total_time = np.zeros(len(a))
open2.append(start_dest)

path = []#Final Path
lat = []#list of latitudes
lon = []#list of longitudes

g[start_dest] = 0
total_time[start_dest] = 0
while len(open1)>0:
	x,y = open1.pop()
	#print (y)
	if y==end_dest:
		print ('Path Found')
		path,lat,lon = trace_path(closed,start_dest,end_dest)#tracing path
		break
	else:
		for i in range(len_listofplaces):
			if a[y][i]!=0:
				if i in open2: 								#Child is in open
					for u,j in open1:
						if j == i:
							if u >(g[y] + a[y][i]+compdis(i,end_dest)):
								open1.remove((u,j))
								g[i] = g[y] + a[y][i]  #Increasing g
								#total_time[i] = total_time[y] + float(timefunc(y,i)) #calculating total time
								open1.append(((g[i]+compdis(i,end_dest)),i)) #f = g + h(compdis)
							else:
								break
				elif i in closed:							#Child is in closed
					for j in closed:
						if j[0] == i:
							if j[1]>(g[y] + a[y][i]+compdis(i,end_dest)):
								closed.remove(j)
								g[i] = g[y] + a[y][i] 	#Increasing g
								#total_time[i] = total_time[y] + timefunc(y,i)  #calculating total time
								open1.append(((g[i]+compdis(i,end_dest)),i)) #f = g + h(compdis)
								#heappush(open1,(a[y][i]+compdis(i,end_dest)))
								open2.append(i)
							else:
								break
				else:										#Child is not open nor closed
					g[i] = g[y] + a[y][i]				#Increasing g
					#total_time[i] = total_time[y] + timefunc(y,i)		#calculating total time
					open1.append(((g[i]+compdis(i,end_dest)),i))		#f = g + h(compdis)
					#heappush(open1,(a[y][i]+compdis(i,end_dest)))
					open2.append(i)

		'''
		Sorting the queue based on its score
		'''
		open1 = sorted(open1,reverse = True)
		#print (open1)
		closed.append((y,x)) #Considered Nodes goes into CLosed


#x = timefunc(start_dest,end_dest)
timefunc(start_dest,end_dest) # Calculating the total time


path.reverse()
z=1
url = 'https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes?'
for i in path:
	df=pd.read_csv('cordinates.csv')
	url = url + 'wp.' + str(z) + '='
	url = url + str(df.iloc[i]['latitude']) + ','
	url = url + str(df.iloc[i]['longitude']) + '&'
	z = z+1


url = url + 'ms=1920,1080&key=Aq8LlcKLQyS0vyUEhI7Zg-KXeH7SZeJ9o8vJtrZ92_fi_NCcS3W8FY_jgh53RdaI'
print(url)


'''
Code Snippet to Map Solution on google maps
'''
gmap = gmplot.GoogleMapPlotter((lat[0]+lat[-1])/2, (lon[0]+lon[-1])/2, 12)
gmap.plot(lat, lon, 'cornflowerblue', marker=True, edge_width=7)
gmap.scatter(lat, lon, '#FF0000', size=180, marker=False)
gmap.scatter(lat, lon, '#8B0000', size=240, marker=False, c=None, s=None)
gmap.draw('map.html')
print(path)
