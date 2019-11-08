''' Name(s): Cameron Fritz
             Ibrahim Elsaid
             Jashanpreet Singh
    
    Project: ParkHere
    Python version: python 3
    
    File Name: distanceCalculate.py
    Purpose: set of functions to calculate the distance between points
    Version: 1.0
    
    Dependencies: parkinggarage.py, googlemaps, geocoder, geopy

    Start Date: 4/30/19
    Last Updated: 6/2/19 
    '''

import googlemaps
from gmplot import gmplot
from geopy.geocoders import Nominatim
import geocoder
from parkinggarage import ParkingGarage
import pickle
import os

def testValidity(text):
    pass
    ''' Simple function that checks to make sure input is valid 
    
        Parameter(s): text - String to be tested
        Return(s): Boolean - whether the text passed the tests or not
    '''
    tests = ["", "!", "?", "[", "]", "}", "{", "@", "#", "$", "%", "^", "*", "+", "="]
    text = text.strip()
    for i in text:
        for test in tests:
            if i == test:
                return False
    
    return True

def findDirections(coords, destination):
    ''' findDirections: Gets the route to the destination

        Parameter(s): destination - string with address to parking garage
        Return: None - if no steps or an error
                coordList - a list of coordinate pairs for each turn on the route 
    '''
    gmaps = googlemaps.Client(key = "AIzaSyDPOAePgFbDCBU0rsOdvWX66C2CPUB2CZM")
    #Make sure the input is valid
    if destination == "":
        g = geocoder.ip("me")
        destination = g.latlng
    else:
        if not testValidity(destination):
            return None
    
    #Get the directions for the route
    try:
        routes = gmaps.directions(coords, destination)
    except googlemaps.exceptions.ApiError:
        print("Hello")
        return None
    #Parsing through the return data to find the steps in the route
    route = routes[0]
    info = route["legs"]
    info = info[0]
    steps = info["steps"]
    # get each coordinate pair and add it to a list
    coordList = []
    for step in steps:
        coordList.append(step['start_location'])
    #Return the list of coordinates
    return coordList

def travelTime(origin, destination):
    ''' travelTime calculates the time it would take to drive to the user's destination

        Parameter(s): origin - String for the user's current location
                      destination - String for the user's target destination
        Return(s): A tuple with two strings
                      time - The time it will take to get to the location
                      distance - The length in miles to the destination
    '''
    gmaps = googlemaps.Client(key = "AIzaSyDPOAePgFbDCBU0rsOdvWX66C2CPUB2CZM")#API key initializes google maps
    if destination == "":
        g = geocoder.ip("me")
        destination = g.latlng
    else:
        if not testValidity(destination):
            return ("Please enter a valid address", "")
    time = ""
    distance = ""
    #Get the route to the destination
    try:
        routes = gmaps.directions(origin, destination)#Get the directions from the location to the destination
    except googlemaps.exceptions.ApiError:#If an invalid location is given
        return ("Please enter a valid address", "")#Return and let them know
    
    #Go through the routes and find the duration and distance to the destination
    route = routes[0]
    legs = route["legs"]
    item = legs[0]
    try:
        x = item["duration"]
        if (x['value'] > 3600):
            return("This destination is out of the range of Drexel","Sorry for the inconvience")
        time = ("It will take: \n" + x['text'] + " to reach " + destination)
    except:
        time = ""
    try:
        x = item["distance"]
        distance = (destination + " is " + x['text'] + " away")
    except:
        distance = ""
    #Return the time and distance
    travelInfo = (time, distance)
    return travelInfo

def walkingDistance(origin):
    ''' walkingDistance calculates the distance between the user's destination
        and all of the surrounding parking garages. It then determines the closest one and returns that

        Parameter(s): origin - String that holds the location of the user's destination
        Return(s): a tuple with three parts:
                    p1 - A string with information on the closest garage
                    p2 - A string with information on the time to the garage
                    minName - the closest garage item itself
    '''
    if origin == "":
        g = geocoder.ip("me")
        origin = g.latlng
    else:
        if not testValidity(origin):
            return ("Please enter a valid address", "", None)
    gmaps = googlemaps.Client(key = "AIzaSyDPOAePgFbDCBU0rsOdvWX66C2CPUB2CZM")#API key initializes google maps
    files = os.listdir("garages")#Gets all of the garage files
    for file in files:#Each file in the list of files
        parts = file.split(".")
        if parts[-1] != "pkl":#If file is not a pickle file
            files.remove(file)#Remove the file

    garages = {}#Empty dict for garages
    
    for file in files:#For each file
        file_path = os.path.join("garages", file)#Set the file path
        item = pickle.load(open(file_path, "rb"))#Load the garage object at the file path
        destination = item.getLocation()#Get the address of the garage
        try:
            routes = gmaps.directions(origin, destination, mode = "walking")#Get the directions from the location to the garage
        except googlemaps.exceptions.ApiError:#If an invalid location is given
            return ("Please enter a valid address", "", None)#Return and let them know
        route = routes[0]
        legs = route["legs"]
        thing = legs[0]
        test = thing["duration"]#get the duration dictionary
        duration = test.get("value")#get the value in seconds from the duration dictionary
        garages[item] = duration
    
    min = 0#Min value
    minName = ""#Item that has min value
    for item in garages:#For each entry in garages
         if garages[item] < min or min == 0:#if the value is less than min or min is 0
             min = garages[item]#Set a new min
             minName = item#Set the min to the item with that value
            
    p1 = ("\nClosest Garage:\n" + str(minName))#Prints the closest garage
    min = round((min/60))
    if min == 1:
        p2 = ("It would take " + str(min) + " minute to get there from your destination")
    else:
        p2 = ("It would take " + str(min) + " minutes to get there from your destination")
    return (p1, p2, minName)

if __name__== "__main__":
    uh = travelTime("115 N. 32nd Street", "1001 W Courtland St, Philadelphia PA")
    #findDirections((39.956896, -75.187936), "3675 Market Street")
    #walkingDistance("115 N. 32nd Street")

    print(testValidity("?"))