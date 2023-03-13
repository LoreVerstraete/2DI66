import numpy as np 

class customer:
    # arrival rate of the customers - group size of those arrivals, which is geometrically distributed with mean 3
    # time in between arrival and queueing 
    
    def arrivaltime(poissonrate, totalTime): 
        '''
        Calculates all the times when groups arrive.
        param poissonrate: at which mean time rate the groups arrive 
        param totalTime: Time of the simulation given in seconds
        return: a list of all the arrival times
        '''
        TimesGroupArrives = []
        t = np.random.poisson(60/poissonrate)      
        while(t < totalTime):
            TimesGroupArrives.append(t)
            t += np.random.poisson(60/poissonrate)
        return TimesGroupArrives
    
    
    def arrive(poissonrate, totalTime, meangroupsize):
        '''
        Puts groupsize and arrival time in a dictonary
        param poissonrate: at which the groups arrive 
        param totalTime: Time of the simulation given in seconds
        param meangroupsize: integer of the mean group size 
        returns: a dictonary of all the people that are comming to the canteen 
        '''
        arrivalTimeArray = customer.arrivaltime(poissonrate, totalTime)
        Customers = {}
        peopleAlreadyInTheCanteen = 0
        groupNr = 1
        for i in range(len(arrivalTimeArray)): 
            groupsize = np.random.geometric(1/meangroupsize)
            for j in range(groupsize): 
                Customers[(j + peopleAlreadyInTheCanteen)] = [groupNr, arrivalTimeArray[i]]
            peopleAlreadyInTheCanteen += groupsize
            groupNr += 1
        return Customers
        # calculate group size (geometric) Mean: meangroupsize
        # calculate arrival rate (poisson) mean: poissonrate
        # output arrival times per person in an array      


    def takeFood(mean, Customers):
        '''
        Calculates how long it takes a person to get the food.
        param mean:  mean of the exponential distribution. 
        returns: a dictonary of all the people that arrived during the time in the Canteen 
        '''
        peopleInTheCanteen = len(Customers)
        for i in range(peopleInTheCanteen): 
            timeToGetFood = np.random.exponential(mean)
            timeToQueue = Customers[i][1]+timeToGetFood 
            Customers[i].append(timeToGetFood)
            Customers[i].append(timeToQueue)
        return Customers
        # exponentially distributed amount of time with a mean of 80 seconds
        # output how long it takes between arrival and queue


    def cardcash(percentagecash, Customers):
        '''
        Decides if the customer pays with cash or a card. 
        param percentagecash: int between 0 and 1
        returns: the dictonary Customers with the addes value cash or card
        '''
        peopleInTheCanteen = len(Customers)
        for i in range(peopleInTheCanteen):
            randomnumber = np.random.uniform(low=0.0, high=1.0)
            if randomnumber <= percentagecash: 
                Customers[i].append("cash")
            else:
                Customers[i].append("card")
        return Customers
        # 40% cash
        # output cash or card
        
    def groupReduceFifteenPercent(customers):
        '''
        Reduces the dictonary by fifteen percent. 
        param customers: dictonary with all the customer that arrive.  
        returns: the reduced dictonary. 
        '''
        amountOfGroups = list(customers.values())[-1][0]
        fifteenPercent = round(amountOfGroups*0.15)
        customers = list(map(list, customers.items())) #changes into a list 
        for i in range(fifteenPercent):
            deletedGroup = np.random.randint(amountOfGroups)
            for j in range(len(customers)-1,0,-1):
                if customers[j][1][0] == deletedGroup:
                    del customers[j]
        reducedCustomersDictonary = dict(customers)
        newlySortedDict = {}  
        for value in range(len(customers)):  
            item = list(reducedCustomersDictonary.values())[value] 
            key, value = value, item  
            newlySortedDict[key] = value  
        return newlySortedDict

# 0: arrival
# 1: take food
# 2: start to queue
# 3: card/cash
