from service import service
from customer import customer
from numpy import zeros, mean, random, std, sqrt, var, linspace, array
#from numpy.ndarray import flatten
import time
import matplotlib.pyplot as plt

import pandas as pd

class simulation:
    # simulate use cases
    # for 1 hour: 12.00h-13.00h

    
    def sim(extension, poissonratearrivals, totalTime, meangroupsize, meanFood, cashpayments, meancash, meancard):

        
        # First the arrival times are determined
        customers = customer.arrive(poissonratearrivals, totalTime, meangroupsize)
        # Output: for 1 customer (customernumber, [GroupNr, arrivalTime, timeToTakeFood, timeToQueue])
        
        # For extension 2 less groups arrive and thus a adjusted set of arrivals is used
        actuallPercentage = 0 
        if extension == 2: 
            customers, actuallPercentage = customer.groupReduceFifteenPercent(customers)
        # Adds to a customer the time it takes to take food
        customersGottenFood = customer.takeFood(meanFood, customers)
        # Output: for 1 customer (customernumber, [GroupNr, arrivalTime, timeToTakeFood, timeToQueue])
        
        # Adds to a customer if the person pays with cash or card
        customersCashCard = customer.cardcash(cashpayments, customersGottenFood)
        # Output: for 1 customer (customernumber, [GroupNr, arrivalTime, timeToTakeFood, timeToQueue, 'card' or 'cash'])
        
        
        # Initialise
        timeCurrent = 0 #start at t=0
        amountOfQueues = 3
        # Create an empty list per queue to be able to assign customers to a queue
        queues = [[] for i in range(amountOfQueues)]
        # Create an empty list per queue to be able to store the finishing times
        timeFinished = [[] for i in range(amountOfQueues)] 
        # Create an array of zeros to keep track of the number of finished customers per queue
        finishedCustomers = zeros(amountOfQueues)
        
        # Sort the customers based on the time they arrive at the queue
        customerInfoSortqueue = sorted(customersCashCard.items(),key=lambda item: (item[1][3]))
        
        # start with an empty list to store all customer info
        listAll = [] 
        for i in range(len(customerInfoSortqueue)):
            # Set new time to time a customer arrives at the queues
            timeToQueue = customerInfoSortqueue[i][1][3]
            if timeCurrent <= timeToQueue:
                timeCurrent = timeToQueue
            
            # Update the queues: check for each queue if customers left the queue before the current time
            for j in range(len(queues)):
                finishedCustomers[j], queues[j] = service.removeFromQueue(timeCurrent, timeFinished[j], finishedCustomers[j], queues[j])
        
            # Assign the customer to the shortest queue
            customerInfoIndiv, queues = service.assignToQueue(queues, customerInfoSortqueue[i])
            # customerInfoIndiv output per customer: (customernumber, [GroupNr, arrivalTime, timeToTakeFood, timeToQueue, 'card' or 'cash', queue Nr])
            
            # Calculate the waiting time for the customer
            customerInfoIndiv = service.waitQueue(queues,customerInfoIndiv,timeFinished)
            # customerInfoIndiv output per customer: (customernumber, [GroupNr, arrivalTime, timeToTakeFood, timeToQueue, 'card' or 'cash', queue Nr, waitingTime])
                        
            # Calculate the service time for the customer
            customerInfoIndiv = service.servicetime(extension, meancash, meancard,customerInfoIndiv)
            # customerInfoIndiv output per customer: (customernumber, [GroupNr, arrivalTime, timeToTakeFood, timeToQueue, 'card' or 'cash', queue Nr, waitingTime, serviceTime])
            
            # Calculate the time a customer is finished
            customerInfoIndiv, TimeFinished = service.finish(customerInfoIndiv, timeFinished)  

            # customerInfoIndiv output per customer: (customernumber, [GroupNr, arrivalTime, timeToTakeFood, timeToQueue, 'card' or 'cash', queue Nr, waitingTime, serviceTime, FinishedTime])

            
            # Append all the information of a individual customer to a list
            listAll.append(customerInfoIndiv)
        

        # Define when the queues are empty
        timeEndEmptyQueue = [max(timeFinished[i]) for i in range(amountOfQueues)]
        timeEndEmptyQueues = max(timeEndEmptyQueue)

        return timeEndEmptyQueues, listAll, actuallPercentage
    
    
    
              
# sim = simulation.sim(simulation.extension, simulation.poissonratearrivals, simulation.totalTime, simulation.meangroupsize, simulation.meanfood, simulation.cashpayments, simulation.meancash, simulation.meancard)
# # sim = simulation.sim(simulation.poissonratearrivals, simulation.totalTime, simulation.meangroupsize, simulation.meanfood, 0, simulation.meancash, simulation.meancard)
# all_results = simulation.results(sim) 
# # question3 = simulation.question3(50)    
