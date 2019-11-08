''' Name(s): Cameron Fritz,
             Ibrahim Elsaid,
             Jashanpreet Singh
    
    Project: Park Here
    Python Version: python3

    File: garageadder.py
    Purpose: Back-end file that allows the adding of parking garage objects
    Version: 1.0

    Start Date: 4/26/19
    Last Updated: 5/6/19
'''

from parkinggarage import ParkingGarage
import pickle
import os

def garageAdder():
    ''' garageAdder creates a garage in the garages directory based on a series of inputs

        Parameters: None
        Returns: None
        Assumptions: a directory called garages 
    '''
    #get the name and the address based on input
    location = input("Enter the address of the garage: ")
    name = input("Enter the name of the garage: ")
    price = {}
    print("Enter prices. Enter q to stop")

    #Continuosly ask for price pairs and add them to a dictionary
    #Don't let the user quit if the dictionary is empty
    while True:
        hour = input("At what hour mark is this price: ")
        if hour == "q":
            if len(price) == 0:
                print("Must have a price")
                continue
            break
        hourPrice = input("What is the price at this hour mark: ")
        print()
        if hourPrice == "q":
            if len(price) == 0:
                print("Must have a price")
                continue
            break
        #Float the price pairs and then add them
        try:
            hour = float(hour)
            hourPrice = float(hourPrice)
            price[hour] = hourPrice
        except ValueError:
            print("Please enter a valid price pair.")
    #Optionally add ratings for availibility and safety
    addRating = input("Would you like to add ratings? (y/n) ")
    if addRating == "y":
        rating = input("What is the availibility? (1-5) ")
        safety = input("What is the safety? (1-5) ")
        print()
    else:
        rating = 2.5
        safety = 2.5
    try:
        rating = float(rating)
        safety = float(safety)
    except ValueError:
        print("Invalid input, diverting to default")
        rating = 2.5
        safety = 2.5
    #Create a new garage object and store it in the garages directory
    newGarage = ParkingGarage(location, name, price, rating, safety)
    file_path = os.path.join("garages", newGarage.getName() + ".pkl")
    pickle.dump(newGarage, open(file_path, "wb"))
    
def removeGarage(garageName):
    ''' removeGarage deletes a garage from storage

        Parameters: garageName - String of the garage name you wish to delete
        Returns: None
        Assumptions: A directory named garages is in the current directory
    '''
    #Get a list of all the files in the garages directory
    path = "garages"
    files = os.listdir(path)
    for name in files:
        namelist = name.split(".")
        #if the file name is the same as the garageName - remove it and break
        if garageName == namelist[0]:
            file_path = os.path.join("garages", garageName + ".pkl")
            os.remove(file_path)
            break
        
    
def updateGarage(name):
    ''' updateGarage allows the user to make changes to an already made garage

        Parameter(s): name - string with the name of the garage
        Return(s): None
        Assumption(s): A directory called garages exists in this one 
    '''
    #Get the garage specified
    path = "garages"
    files = os.listdir(path)
    object = None
    for item in files:
        if item == (name + ".pkl"):
            file_path = os.path.join("garages", item)
            object = pickle.load(open(file_path, "rb"))
            break
    if object == None:
        print("Garage not found")
        return
    #Get what the user wants to update
    print("a. address\nb. name\nc. prices\nd. availibility\ne. safety")
    ask = input("What would you like to change? ")
    if ask == "a":
        ask = input("What is the new address? ")
        object.setLocation(ask)
    elif ask == "b":
        os.remove(file_path)
        ask = input("What is the new name? ")
        object.setName(ask)
    elif ask == "c":
        prices = {}
        print("Enter q to quit")
        #Continously ask for price pair
        while True:
            try:
                hour = float(input("At what hour mark is this price: "))
                if hour == "q":
                    if len(prices) == 0:
                        print("Must have a price")
                        continue
                    break
                hourPrice = float(input("What is the price at this hour mark: "))
                print()
                if hourPrice == "q":
                    if len(prices) == 0:
                        print("Must have a price")
                        continue
                    break
                prices[hour] = hourPrice
            except ValueError:
                print("Invalid price pair")
        object.setPriceList(prices)
    elif ask == "d":
        ask = input("What is the availibility rating? ")
        try:
            ask = float(ask)
            if ask > 5 or ask < 0:
                raise ValueError
            object.setAvailibility(ask)
        except ValueError:
            print("Invalid availibility")
    elif ask == "e":
        ask = input("What is the safety rating? ")
        try:
            ask = float(ask)
            if ask > 5 or ask < 0:
                raise ValueError
            object.setSafety(ask)
        except ValueError:
            print("Invalid safety")
    #Put the new file in the garages directory
    file_path = os.path.join("garages", object.getName() + ".pkl")
    pickle.dump(object, open(file_path, "wb"))
    
    
if __name__ == "__main__":
    print("Use this script to add or delete garage objects")
    #continuosly get input until an exit call
    while True:
        print("a. Add a garage")
        print("b. Delete a garage")
        print("c. Print all garages")
        print("d. Update a garage")
        print("e. Exit")
        ans = input("What would you like to do? ")
        print()
        if ans == "e":
            #exit program
            print("Good-bye")
            break
        elif ans == "a":
            #add garage
            garageAdder()
        elif ans == "b":
            #delete a garage
            name = input("What garage to delete? ")
            removeGarage(name)
        elif ans == "c":
            #Get a list of all the garages and display them
            List = []
            path = "garages"
            files = os.listdir(path)
            for name in files:
                namelist = name.split(".")
                if namelist[-1] == "pkl":
                    #Make sure that the file is a pickle file
                    file_path = os.path.join("garages", name)
                    List.append(pickle.load(open(file_path, "rb")))
            for item in List:
                print(item)
            print()
        elif ans == "d":
            #Update a garage
            ask = input("What garage would you like to update? ")
            updateGarage(ask)