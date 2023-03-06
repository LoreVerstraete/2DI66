import numpy as np 

class customer:
    # arrival rate of the customers - group size of those arrivals, which is geometrically distributed with mean 3
    # time in between arrival and queueing 
    
    def arrivaltime(poissonrate, totalTime): 
        '''
        Calculates all the times when groups arrive.
        param poissonrate: at which the groups arrive 
        param totalTime: Time of the simulation given in seconds
        return: an Array of the arrival time of the groups
        '''
        TimesGroupArrives = []
        t = np.random.poisson(poissonrate)
        while(t < totalTime):
            TimesGroupArrives.append(t)
            t += np.random.poisson(poissonrate)
        return TimesGroupArrives


    def groupsize(meangroupsize):
        ''' 
        Calculates the group size of the arriving group. 
        param meangroupsize: integer of the mean group size 
        returns: the arrival time of each person
        '''
        groupsize = np.random.geometric(1/meangroupsize)
        return groupsize
    
    
    def arrive(poissonrate, totalTime, meangroupsize):
        '''
        Puts groupsize and arrival time in a 2D-Array.
        param poissonrate: at which the groups arrive 
        param totalTime: Time of the simulation given in seconds
        param meangroupsize: integer of the mean group size 
        returns: 2D-Array with the format [[arivall time, Groupsize],[arivall time, Groupsize],... ]
        '''
        arrivalTimeArray = customer.arrivaltime(poissonrate, totalTime)
        arrival = []
        for i in range(len(arrivalTimeArray)): 
            groupsize = customer.groupsize(meangroupsize)
            arrival.append([arrivalTimeArray[i],groupsize])
        return arrival
        # calculate group size (geometric) Mean: meangroupsize
        # calculate arrival rate (poisson) mean: poissonrate
        # output arrival times per person in an array         


    def take_food(mean):
        '''
        Calculates how long it takes a person to get the food
        param mean:  mean of the exponential distribution. 
        returns: time for each person to be in a queue
        '''
        timeToGetFood = np.random.exponential(1/mean)
        return timeToGetFood
        # exponentially distributed amount of time with a mean of 80 seconds
        # output how long it takes between arrival and queue


    def cardcash(percentagecash):
        '''
        Decides if the customer pays with cash or a card. 
        param: percentagecash: int between 0 and 1
        returns: cash (1) or card(2)
        '''
        randomnumber = np.random.uniform(low=0.0, high=1.0)
        if randomnumber <= percentagecash: 
            return 1 # cash
        else:
            return 2 # card
        # 40% cash
        # output cash or card

print(customer.arrive(4, 60,4))