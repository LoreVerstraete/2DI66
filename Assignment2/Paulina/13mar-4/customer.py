import numpy as np 

class customer:
    
    def arrivaltime(poissonrate, totalTime): 
        '''
        Calculates all the times when groups arrive.
        Param poissonrate: at which meantime rate the groups arrive.
        Param totalTime: Time of the simulation given in seconds.
        Return: a list of all the arrival times.
        '''
        TimesGroupArrives = []  #list to save all the different times when groups arrive 
        t = np.random.poisson(60/poissonrate)      
        while(t < totalTime):   # checks that arrival time is within the hour 
            TimesGroupArrives.append(t)
            t += np.random.poisson(60/poissonrate)  # adds new arrival time 
        return TimesGroupArrives
    
    
    def arrive(poissonrate, totalTime, meangroupsize):
        '''
        Puts groupsize and arrival time in a dictionary.
        Param poissonrate: at which the groups arrive.
        Param totalTime: Time of the simulation given in seconds.
        Param meangroupsize: integer of the mean group size. 
        Returns: a dictionary of all the customers that are coming to the canteen. 
        '''
        arrivalTimeArray = customer.arrivaltime(poissonrate, totalTime)
        Customers = {}  # creates dictonary to save all the information about the customer.
        customerAlreadyInTheCanteen = 0  # keeps track amount of customers in the canteen 
        groupNr = 1  # keeps track of the number of groups that already arrived 
        for i in range(len(arrivalTimeArray)): # goes over all the arrival times for the groups 
            groupsize = np.random.geometric(1/meangroupsize)
            for j in range(groupsize): 
                Customers[(j + customerAlreadyInTheCanteen)] = [groupNr, arrivalTimeArray[i]]
            customerAlreadyInTheCanteen += groupsize
            groupNr += 1
        return Customers  


    def takeFood(mean, Customers):
        '''
        Calculates how long it takes a person to get the food.
        Param mean:  mean of the exponential distribution. 
        Returns: a dictonary of all the customers that arrived during the time in the Canteen 
        '''
        customersInTheCanteen = len(Customers) # calculates the number of all the customers that visit the canteen during lunch break 
        for i in range(customersInTheCanteen): 
            timeToGetFood = np.random.exponential(mean)  # chooses a random number for the time the customer needs to get the food 
            timeToQueue = Customers[i][1]+timeToGetFood  # calculates the time it takes the customer to get to the queue
            Customers[i].append(timeToGetFood)
            Customers[i].append(timeToQueue)
        return Customers 


    def cardcash(percentagecash, Customers):
        '''
        Decides if the customer pays with cash or a card. 
        param percentagecash: int between 0 and 1
        returns: the dictionary customers with the added value cash or card
        '''
        customersInTheCanteen = len(Customers)
        for i in range(customersInTheCanteen):  # goes through all the customers in the canteen during lunch hour 
            randomnumber = np.random.uniform(low=0.0, high=1.0) # picks a random number between 0 and 1 to decide if the customer pays with cash or card 
            if randomnumber <= percentagecash: 
                Customers[i].append("cash")
            else:
                Customers[i].append("card")
        return Customers

        
    def groupReduceFifteenPercent(customers):
        '''
        Reduces the groups in the dictionary by fifteen percent. 
        Param customers: dictionary with all the customers that arrive.  
        Returns: the reduced dictionary. 
        '''
        amountOfGroups = list(customers.values())[-1][0] # number of groups during lunch break 
        fifteenPercent = round(amountOfGroups*0.15)  # calculates 15% of the group 
        actualPercentage = fifteenPercent/amountOfGroups # calculates the actual percentage of the groups that are going to the food cart 
        customers = list(map(list, customers.items())) #changes into a list 
        for i in range(fifteenPercent):
            deletedGroup = np.random.randint(amountOfGroups) # picks a random number for the groups that are not going to the canteen 
            for j in range(len(customers)-1,0,-1):
                if customers[j][1][0] == deletedGroup:
                    del customers[j]  # deleting all the customers from the group 
        reducedCustomersDictonary = dict(customers)
        newlySortedDict = {}  # rearranges dictionary to have a continuous customer number in the key  
        for value in range(len(customers)):  
            item = list(reducedCustomersDictonary.values())[value] 
            key, value = value, item  # assigning new number to the customers 
            newlySortedDict[key] = value  
        return newlySortedDict, actualPercentage

# Order for customer in the canteen 
# 0: arrival
# 1: take food
# 2: start to queue
# 3: card/cash
