''' Name(s): Cameron Fritz,
             Ibrahim Elsaid,
             Jashanpreet Singh,
    
    Project: Park Here
    Python Version: python 3
    
    File: main.py
    Purpose: The main part of the app, creates a kivy applet
    Version: 1.0

    Dependencies: parkinggarage.py, distancecalculate.py, 
                  kivy, kivy-garden, mapview, 
                  googlegeocoder, geocoder, googlemaps

    Start Date: 4/17/19
    Last Updated: 6/2/19
    '''

#Imports
from parkinggarage import ParkingGarage
from distancecalculate import walkingDistance, travelTime, findDirections
from kivy.garden import mapview
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.bubble import Bubble
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.graphics import Scale, Translate, Color, Line
from kivy.uix.screenmanager import ScreenManager, Screen, TransitionBase
import googlemaps
from math import tan, sin, cos, log, pi
from googlegeocoder import GoogleGeocoder
from mapview import MapMarker, MapLayer, MapView, MapMarkerPopup, MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE
from mapview.utils import clamp
import os
import pickle
import random
import geocoder

class ParkingSearch(Screen):
    ''' Screen that allows searching for a parking garage and displays the garages on a map '''
    def displayDist(self):
        ''' Requires input into the text box on screen
            Takes that input and the current location then calculates the closest garage to the destination
            It also shows the distance and time to destination and parking garage 
            
            Parameters: No parameters passed in, but does require text in the textbox on screen
            Returns: The closest ParkingGarage object to the destination
                     if an error occurs - returns None'''
        g = geocoder.ip("me")
        coords = g.latlng
        try:
            #Calls functions that caluclate the distance and catches any error raised by them
            displayText = walkingDistance(self.ids.destination.text) 
            if displayText[2] == None:
                raise ValueError
            distanceTest = travelTime(coords, self.ids.destination.text)
            self.ids.travel.text = (displayText[0] + "\n" + displayText[1])#Change the text of the labels
            self.ids.closest.text = (distanceTest[0] + ",\n" + distanceTest[1])
            #Returns a parking garage object
            return displayText[2]
        except:
            return None
    
    def markDestination(self, destination):
        ''' Takes in a parking garage object called destination
            Gets the location of the destination and places a map marker on top of it 
            
            Parameters: destination - ParkingGarage object
            Returns: coords - tuple with the coordinates of the map marker
        '''
        if  not isinstance(destination, ParkingGarage):
            pop = Popup(title = "Error", content = Label(text = "No Destination Input"), size_hint = (.2, .2))
            pop.open()
            return

        #Get the coordinates of the destination
        coder = GoogleGeocoder("AIzaSyDPOAePgFbDCBU0rsOdvWX66C2CPUB2CZM")
        g = coder.get(destination.getLocation())
        coords = (g[0].geometry.location.lat, g[0].geometry.location.lng)

        #Create a marker that holds information on the parking garage
        bub = Bubble(size_hint = (None, None), size = (200, 50), arrow_pos = 'bottom_left')
        lab = Label(text = ("            " + destination.getName()), text_size = (self.width, None))
        lab.height = lab.texture_size[1]
        lab.halign = 'center'
        bub.add_widget(lab)
        m1 = MapMarkerPopup(lat = coords[0], lon = coords[1], placeholder = bub)
        
        #Mark the map and return the coordinates of the marker
        self.ids.map1.add_marker(m1)
        self.ids.map1.center_on(coords[0], coords[1])
        return coords
    
    def displayAll(self):
        ''' Simple function that displays all parking garages on file 
            Parameters: N/A
            Returns: None 
        '''
        #Get the list of garages, filter for only garage objects, and make sure it is not empty
        garageList = os.listdir("garages")
        for item in garageList:
            parts = item.split(".")
            if parts[-1] != "pkl":
                garageList.remove(item)
        if not garageList:
            pop = Popup(title = "Error", content = Label(text = "No Garages on File"), size_hint = (None, None), size = (200, 200))
            pop.open()
            return
        
        #For each garage on file, mark its location
        coder = GoogleGeocoder("AIzaSyDPOAePgFbDCBU0rsOdvWX66C2CPUB2CZM")
        for item in garageList:
            item = os.path.join("garages", item)
            gar = pickle.load(open(item, "rb"))
            g = coder.get(gar.getLocation())
            coords = (g[0].geometry.location.lat, g[0].geometry.location.lng)
            m1 = MapMarker(lat = coords[0], lon = coords[1])
            self.ids.map1.add_marker(m1)

class GarageScreen(Screen):
    '''Class that is used to display information on the nearest garage '''
    def mark(self, coords, info):
        ''' mark takes a garage and then marks its location on a map
            It also fills out the information on the screen for the garage

            Parameters: coords - coordinates of the nearest garage
                        info - parking garage object
            Returns: None
        '''

        if info == None:
            return
        
        #Add a marker to the screen and fill out information on the screen
        marker = MapMarker(lat = coords[0], lon = coords[1])
        self.ids.map2.add_marker(marker)
        self.ids.garage.text = str(info)

        #Display the pricing at the garage
        priceText = "Hour : Price"
        priceList = info.getPriceList()
        for item in priceList:
            priceText += "\n" + str(item) + " : " + str(priceList[item])
        self.ids.prices.text = priceText
    
    def displayRoute(self, destination):
        ''' 
            displayRoute aims to show the route that the user would have to take to get to the garage
        
            WORK IN PROGRESS
            Currently does get the directions and places a marker for each turn, 
            but does not properly show the route as intended.
            Decision to not implement this as it would prove distracting to the user in is current state.

            Parameter(s): destination - String that holds the address of the nearest parking garage
            Return(s): None
        '''
        #Get the directions to the address
        g = geocoder.ip("me")#Get the location based on IP address
        coords = g.latlng#Get the coordinates of my location
        directions = findDirections(coords, destination)
        if directions == None:
            print("No directions available")
            return
        
        #Mark each point
        for point in directions:
            mark = MapMarker(lat = point["lat"], lon = point["lng"])
            self.ids.map2.add_marker(mark)

Builder.load_string("""
#: import MapSource mapview.MapSource
<ParkingSearch>:
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            size_hint_y: .1
            TextInput:
                id: destination
                hint_text: "What is your destination?"
                font_size: 30
                height: 60
            Button:
                text: "Find Parking"
                size_hint_x: .2
                on_press:
                    info = root.displayDist()
                    coords = root.markDestination(info)
                    root.manager.get_screen("map").mark(coords, info)
        MapView:
            size_hint_y: .7
            id: map1
            zoom: 16
            lat: 39.9566
            lon: -75.1899
        BoxLayout:
            size_hint_y: .2
            Button:
                text: "More Information About the Closest Garage"
                on_press:
                    root.manager.current = "map"
            Button:
                text: "Other Garages in the Area"
                on_press:
                    root.displayAll()
        BoxLayout:
            size_hint_y: None
            size_y: 100
            Label:
                id: closest
                text: ""
            Label:
                id: travel
                text: ""
<GarageScreen>:
    BoxLayout:
        orientation: "vertical"
        MapView:
            id: map2
            zoom: 15
            lat: 39.9566
            lon: -75.1899
        BoxLayout:
            size_hint_y: .25
            Label:
                id: garage
                text: ""
            Label:
                id: prices
                text: ""
        BoxLayout:
            size_hint_y: .2
            Button:
                text: "Back"
                on_press:
                    root.manager.current = "search"
""")

#The App itself
class ParkHereApp(App):
    def build(self):
        ''' Called automatically when the app is created
            Parameter(s): None
            Return(s): sm - a screen manager that holds the screens
        '''
        #Create a holder for the screens, add the screens, and set the transition between screens to None
        sm = ScreenManager()
        sm.transition = TransitionBase()
        sm.add_widget(ParkingSearch(name = 'search'))
        sm.add_widget(GarageScreen(name = 'map'))
        return sm

if __name__ == "__main__":
    ParkHereApp().run()#Create and run the app