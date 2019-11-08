''' Name: Ibrahim Elsaid
    Project: Park Here

    Project: Park Here
    Python Version: python 3

    File: parkinggarage.py
    Purpose: file with a parking garage class. This class is used for creating objects that hold data on parking garages
    Version: 1.0

    Start Date: 4/15/19
    Last Updated: 4/17/19
'''

class ParkingGarage:
    '''This class is a class designed to represent a Parking Garage

    It intakes:
        location
        price
        name
        availibility(1-5) - has a default of 2.5
        safety(1-5) - has a default of 2.5
        '''
    
    #Init method takes in the four parameters listed above
    def __init__(self, location, name, price, availibility = 2.5, safety = 2.5):
        ''' Init method called when the object is made

            Parameter(s): location - the address
                          name - name of the garage
                          price - dictionary of all the prices
                          availability - float out of 5 for the availibility of the garage
                          safety - float out of 5 for the safety of the garage
            Return(s): 
        '''
        self.__location = location #string 
        self.__prices = price #dict type. The key corisponds to the minimum hour needed to stay for that price
        self.__name = name #string
        self.__availibility = availibility #float
        self.__safety = safety #float
    
    #Getters
    def getLocation(self):
        return self.__location
    
    def getName(self):
        return self.__name
    
    #Intakes an hour that the user will stay at the parking garage and returns the price
    def getPriceHour(self, hour):
        hour = int(hour)
        payedPrice = 0
        for price in self.__prices:
            if hour >= price:
                payedPrice = self.__prices.get(price)
            elif hour <= 1:
                payedPrice = self.__prices[1]
                break
        return payedPrice
        
    def getPriceList(self):
        return self.__prices
    
    def getAvailibility(self):
        return self.__availibility
    
    def getSafety(self):
        return self.__safety
    
    #Setters
    def setLocation(self, location):
        self.__location = location
        
    def setPriceList(self, prices):
        self.__price = prices
    
    def setAvailibility(self, avail):
        self.__availibility = avail
        
    def setSafety(self, safety):
        self.__safety = safety
        
    #Enables the object to be printed
    def __str__(self):
        return str(self.__name) + " is at " + str(self.__location) + "\nHas a " + str(self.__safety) + " star safety rating \nHas a " + str(self.__availibility) + " star availibility rating."
    
if __name__ == "__main__":
    prices = {1: 2.5, 2: 5.0, 3: 7.5, 4: 10.0, 8: 15.0}
    lotS = ParkingGarage("123 South St.", "Lot S", prices)
    print("Lot name is:", lotS.getName())
    print("Lot location is:", lotS.getLocation())
    print("Lot price list is:", lotS.getPriceList())
    print("Price at .5 hours", lotS.getPriceHour(.5))
    print("Price at 6 hours", lotS.getPriceHour(6))
    
    print(lotS)
    