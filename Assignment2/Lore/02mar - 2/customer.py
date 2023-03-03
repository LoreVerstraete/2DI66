from numpy import zeros, random

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
        t = random.poisson(poissonrate)
        while(t < totalTime):
            TimesGroupArrives.append(t)
            t += random.poisson(poissonrate)
        return TimesGroupArrives


    def groupsize(meangroupsize):
        ''' 
        Calculates the group size of the arriving group. 
        param meangroupsize: integer of the mean group size 
        returns: the arrival time of each person
        '''
        groupsize = random.geometric(1/meangroupsize)
        return groupsize
    
    
    def arrive(poissonrate, totalTime, meangroupsize):
        '''
        Puts groupsize and arrival time in a 2D-Array
        param poissonrate: at which the groups arrive 
        param totalTime: Time of the simulation given in seconds
        param meangroupsize: integer of the mean group size 
        returns: 2D-Array with the format [[arivall time, Groupsize],[arivall time, Groupsize],... ]
        '''
        arrivalTimeArray = customer.arrivaltime(poissonrate, totalTime)
        arrival = []
        arrival_group = []
        for i in range(len(arrivalTimeArray)): 
            groupsize = customer.groupsize(meangroupsize)
            arrival.append([arrivalTimeArray[i],groupsize])
            arrival_group.append([arrival[i][0]]*arrival[i][1])
        arrival_individual = [item for sublist in arrival_group for item in sublist]
        return arrival_individual,arrival_group, arrival
        # calculate group size (geometric) Mean: meangroupsize
        # calculate arrival rate (poisson) mean: poissonrate
        # output arrival times per person in an array         


    def take_food(mean,arrival_individual):
        '''
        Calculates how long it takes a person to get the food
        param mean:  mean of the exponential distribution. 
        returns: time for each person to be in a queue
        '''
        foodtaken_individual =zeros(len(arrival_individual))
        for i in range(len(arrival_individual)):
            timeToGetFood = random.exponential(mean)
            foodtaken_individual[i] = arrival_individual[i] + timeToGetFood
        return foodtaken_individual
        # exponentially distributed amount of time with a mean of 80 seconds
        # output how long it takes between arrival and queue


    def cash(fractioncash):
        '''
        Decides if the customer pays with cash or a card. 
        param: fractioncash: int between 0 and 1
        returns: cash (1) or card(2)
        '''
        randomnumber = random.uniform(low=0.0, high=1.0)
        if randomnumber <= fractioncash: 
            cash = True # cash
        else:
            cash = False # card
        return cash
        # 40% cash
        # output cash or card
    
    def customer_info(arrival_individual,foodtaken_individual,fractioncash):
        customer_info = {}
        for i in range(len(arrival_individual)):
            customer_info[i]={'t_arrival':arrival_individual[i],'t_foodtaken':foodtaken_individual[i], 'cash': customer.cash(fractioncash)}
        return customer_info
    
# print(customer.cash(0.4))
# print(customer.take_food(80, [1,40]))
# print(customer.arrive(4, 60,4))
# customerinfo = customer.customer_info([0,30],[40,50],0.4)
# print(customerinfo[0]['cash'])