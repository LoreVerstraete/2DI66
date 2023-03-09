from service import service
from customer import customer
from numpy import zeros, mean, random, std, sqrt, var, linspace, array
#from numpy.ndarray import flatten
import time
import matplotlib.pyplot as plt

class simulation:
    # simulate use cases
    # for 1 hour: 12.00h-13.00h

    poissonratearrivals = 1 #TODO in minutes make sure that the units are everwhere the same  
    meangroupsize = 3
    meanfood = 80 #seconds
    total_nr_queues = 3
    list_queued_customers_old = zeros(total_nr_queues)
    total_time = 3600 # in seconds 
    cashCard = 0.4
    meancard = 15
    meancash = 20
    

    
    def sim(poissonratearrivals, totalTime, meangroupsize, meanFood, cashCard,meancash, meancard):
        Customers = customer.arrive(poissonratearrivals, totalTime, meangroupsize)
        CustomersGottenFood = customer.take_food(meanFood, Customers)
        CustomersCashCard = customer.cardcash(cashCard, CustomersGottenFood)
        
        # Initialise
        TimeCurrent = 0 #start at t=0
        amount_of_queues = 3
        Queues = [[] for i in range(amount_of_queues)]
        TimeFinished = [[] for i in range(amount_of_queues)]
        FinishedCustomers = zeros(amount_of_queues)
        
        customer_info_sortqueue = sorted(CustomersCashCard.items(),key=lambda item: (item[1][3]))
        
        listAll = []
        for i in range(len(customer_info_sortqueue)):
            # Set new time to time a customer arrives at the queues
            TimeToQueue = customer_info_sortqueue[i][1][3]
            if TimeCurrent <= TimeToQueue:
                TimeCurrent = TimeToQueue
            
            # Update the queues: check for each queue if customers left the queue before the current time
            for j in range(len(Queues)):
                FinishedCustomers[j],Queues[j] = service.remove_from_queue(TimeCurrent, TimeFinished[j], FinishedCustomers[j], Queues[j])
            
            # Assign the customer to the shortest queue
            customer_info_indiv, Queues = service.assign_to_queue_indiv(Queues, customer_info_sortqueue[i])
            
            # Calculate the waiting time for the customer
            customer_info_indiv = service.wait_queue(Queues,customer_info_indiv,TimeFinished)

                        
            # Calculate the service time for the customer
            customer_info_indiv = service.servicetime_indiv(meancash, meancard,customer_info_indiv)

            
            # Calculate the time a customer is finished
            customer_info_indiv, TimeFinished = service.finish(customer_info_indiv, TimeFinished)

            listAll.append(customer_info_indiv)
        TimeEndEmptyQueue = [max(TimeFinished[i]) for i in range(amount_of_queues)]
        TimeEndEmptyQueues = max(TimeEndEmptyQueue)

        return TimeEndEmptyQueues, listAll
    
    
    def results(sim):
        GroupNr = 0
        ArrTime = 1
        TimeFood = 2
        TimeQueue = 3
        CashCard = 4
        nrQueue = 5
        WaitTime = 6
        ServiceTime = 7
        FinishTime = 8
   
        
        # Question 1
        print("Question 1 ")
        # Sojourn time arbitrary customer (individual)
        i = random.randint(0,len(sim[1]))
        sojourn_time = sim[1][i][1][FinishTime] - sim[1][i][1][ArrTime]
         
        sojourn_time_individual = []
        for i in range(len(sim[1])):
            sojourn_time_individual.append(sim[1][i][1][FinishTime] - sim[1][i][1][ArrTime])
        plt.hist(sojourn_time_individual, bins =15)
        plt.show()
        
        # Expected time spend waiting in queue
        queue_time_list = []
        for i in range(len(sim[1])):
            queue_time_list.append(sim[1][i][1][WaitTime])
        print("mean waiting time", mean(queue_time_list))
        print("std waiting time", std(queue_time_list))
        
        # Expected number customers in the canteen        
        CustomersInCanteenSeconds = [0 for i in range(int(simulation.total_time))] 
        for i in range(len(sim[1])): 
            j = 0
            for j in range(int(sim[1][i][1][ArrTime]), int(sim[1][i][1][FinishTime])): #change if stepsize is smaller than 1 seconde 
                if 0<j <simulation.total_time:
                    CustomersInCanteenSeconds[j] += 1
        AverageCustomersInCanteen = mean(CustomersInCanteenSeconds)
        StandardDeviationCustomersInCanteen = std(CustomersInCanteenSeconds)
        
        print("Custumers in the canteen each seconde:", AverageCustomersInCanteen )
        print("Standard deviation customers in canteen:", StandardDeviationCustomersInCanteen)
        plt.hist(CustomersInCanteenSeconds,bins=20)
        plt.xlabel("Number of customers")
        plt.ylabel("frequence")
        plt.title("Distribution of customers in the canteen")
        plt.show()
        
        # Question 2
        # sojourn time group
        print("Question 2")
        allGroups = []

        for i in range(len(sim[1])):
            Group = sim[1][i][1][GroupNr]
            if Group not in allGroups:
                allGroups.append(Group)
        
        dictGroups = {}

        for i in allGroups:
            ALLTIME = []
            for g in range(len(sim[1])):
                G = sim[1][g][1][GroupNr]
                if G == i:
                    ArrivalTime = sim[1][g][1][ArrTime]
                    ALLTIME.append(sim[1][g][1][FinishTime])
                    maxTime = max(ALLTIME)
                dictGroups[i] = (ArrivalTime, maxTime)
        sojournGroup = []
        for i in range(len(allGroups)):
            sojournGroup.append(dictGroups[i+1][1] - dictGroups[i+1][0])
        print("Mean sojourn time per group", mean(sojournGroup))
        print("Std sojourn time per group", std(sojournGroup))
        
        
        # Question 3
        # give distribution number customers present in canteen: average, std, histogram
        # see function question 3 
    
        # Question 4
        # arbitrary customer 
        print("Question 4")
        lb1 = mean(sojourn_time_individual) - 1.96*sqrt(var(sojourn_time_individual)/len(sim[1]))
        ub1 = mean(sojourn_time_individual) + 1.96*sqrt(var(sojourn_time_individual)/len(sim[1]))
        print("Half-width arbitrary customer", 1.96*sqrt(var(sojourn_time_individual)/len(sim[1])))
        print("Confidence interval arbitrary customer", lb1, ",", ub1)
        
        # arbitrary group
        lb1 = mean(sojournGroup) - 1.96*sqrt(var(sojournGroup)/len(allGroups))
        ub1 = mean(sojournGroup) + 1.96*sqrt(var(sojournGroup)/len(allGroups))
        print("Half-width arbitrary customer", 1.96*sqrt(var(sojournGroup)/len(allGroups)))
        print("Confidence interval arbitrary customer", lb1, ",", ub1)
        return "finished Simulation"
        
        
    def question3(numberOfRepeats):  
        ArrTime = 1
        FinishTime = 8
        listAll = []
        for i in range(numberOfRepeats):
            sim = simulation.sim(simulation.poissonratearrivals, simulation.total_time, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
            CustomersInCanteenSeconds = [0 for i in range(int(simulation.total_time))] 
            for i in range(len(sim[1])): 
                for j in range(int(sim[1][i][1][ArrTime]), int(sim[1][i][1][FinishTime])): #change if stepsize is smaller than 1 seconde 
                    if 0<j <simulation.total_time:
                        CustomersInCanteenSeconds[j] += 1
            listAll.append(CustomersInCanteenSeconds) 
        listAllarray = array(listAll)
        listAllFlatten = listAllarray.flatten()
        
        plt.hist(listAllFlatten, bins= 40)
        plt.show()
        
        Mean = mean(listAllFlatten) 
        StandardDeviation = std(listAllFlatten)
        print("Question 3")
        print("Mean:", Mean)
        print("Standard deviation:", StandardDeviation)
        return "Question 3 is calculated"
              
sim = simulation.sim(simulation.poissonratearrivals, simulation.total_time, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
all_results = simulation.results(sim) 
question3 = simulation.question3(50)    
