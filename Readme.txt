***Required libraries:***
	pickle
	gmplot
	geopy
	pandas


***File Details***
1. "a.txt" --  List of all the places(localities).
2. "b.txt" -- List of places which were not found on openstreet.org 
3. "cordinates.csv" -- Fetched Lat,Lon of the places listed in "a.txt"
4. "Compute Latitude and Longitude.py" -- Computes Latitude and Longitude using Nominatim(Openstreet Map).
5. "Computing Distance.py" -- Computes distance between localities in cordinates.csv and saves it in adjacency matrix using pickle.
6. "Astar algorithm.py" -- Computes the path and fetches heuristic from Bing maps API.


***Run Procedure***
1. Can run "Astar algorithm.py" file directly as the adjacency matrix and coordinates are already fetched and present.


***Returns***
1. "Astar algorithm.py" -- Distance of path(Km), Total estimated time(seconds), URL for the REST API plot of the path calculated.
