import numpy as np 

class customer:
    # arrival rate of the customers - group size of those arrivals, which is geometrically distributed with mean 3
    # time in between arrival and queueing 
    
    def arrivaltime(poissonrate: int, totalTime: int): 
        '''
        Calculates all the times when groups arrive.
        param poissonrate: at which mean time rate the groups arrive 
        param totalTime: Time of the simulation given in seconds
        return: a list of all the arrival times
        '''
        timesGroupArrives = []
        t = np.random.poisson(60/poissonrate)      
        while(t < totalTime):
            timesGroupArrives.append(t)
            t += np.random.poisson(60/poissonrate)
        return timesGroupArrives
    
    
    def arrive(poissonrate: int, totalTime: int, meangroupsize: int):
        '''
        Puts groupsize and arrival time in a dictonary
        param poissonrate: at which the groups arrive 
        param totalTime: Time of the simulation given in seconds
        param meangroupsize: integer of the mean group size 
        returns: a dictonary of all the customer that are comming to the canteen 
        '''
        arrivalTimeArray = customer.arrivaltime(poissonrate, totalTime)
        customers = {}
        peopleAlreadyInTheCanteen = 0
        groupNr = 1
        for i in range(len(arrivalTimeArray)): 
            groupsize = np.random.geometric(1/meangroupsize)
            for j in range(groupsize): 
                customers[(j + peopleAlreadyInTheCanteen)] = [groupNr, arrivalTimeArray[i]]
            peopleAlreadyInTheCanteen += groupsize
            groupNr += 1
        return customers
        # calculate group size (geometric) Mean: meangroupsize
        # calculate arrival rate (poisson) mean: poissonrate
        # output arrival times per person in an array      


    def takeFood(mean: int, customers: dict):
        '''
        Calculates how long it takes a person to get the food.
        param mean:  mean of the exponential distribution. 
        returns: a dictonary of all the customer that arrived during the time in the Canteen 
        '''
        customersInTheCanteen = len(customers)
        for i in range(customersInTheCanteen): 
            timeToGetFood = np.random.exponential(mean)
           # print(customers[i][1])
            timeToQueue = customers[i][1]+timeToGetFood 
            customers[i].append(timeToGetFood)
            customers[i].append(timeToQueue)
        return customers
        # exponentially distributed amount of time with a mean of 80 seconds
        # output how long it takes between arrival and queue


    def cardcash(percentagecash: float, customers: dict):
        '''
        Decides if the customer pays with cash or a card. 
        param percentagecash: int between 0 and 1
        returns: the dictonary customers with the addes value cash or card
        '''
        peopleInTheCanteen = len(customers)
        for i in range(peopleInTheCanteen):
            randomnumber = np.random.uniform(low=0.0, high=1.0)
            if randomnumber <= percentagecash: 
                customers[i].append("cash")
            else:
                customers[i].append("card")
        return customers
        # 40% cash
        # output cash or card
        
    def groupReduceFifteenPercent(customers: dict):
        '''
        Reduces the dictonary by fifteen percent. 
        param customers: dictonary with all the customer that arrive.  
        returns: the reduced dictonary. 
        '''
        amountOfGroups = list(customers.values())[-1][0]
        fifteenPercent = round(amountOfGroups*0.15)
        customers = list(map(list, customers.items())) #changes into a list 
        for i in range(fifteenPercent):
            randomElement = np.random.randint(amountOfGroups)
            for j in range(len(customers),0):
                if customers[j][0] == randomElement:
                    del customers[randomElement]
        reducedCustomersDictonary = dict(customers)
        print(reducedCustomersDictonary)
        return reducedCustomersDictonary           
        


# 0: arrival
# 1: take food
# 2: start to queue
# 3: card/cash