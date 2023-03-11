from service import service
from customer import customer
from numpy import zeros, mean, random, std, sqrt, var, linspace, array
#from numpy.ndarray import flatten
import time
import matplotlib.pyplot as plt

class simulation:
    # simulate use cases
    # for 1 hour: 12.00h-13.00h

    poissonratearrivals = 1 
    meangroupsize = 3
    meanfood = 80 #seconds
    totalNrQueues = 3
    listQueuedCustomersOld = zeros(totalNrQueues)
    totalTime = 3600 # in seconds 
    cashCard = 0.4
    meancard = 12
    meancash = 20
    modelExtension = 2 # number between 0 and 3 
    # modelextension = 0 no extension, 1 first extension, 2 seconde extension, 3 third extension 
    

    
    def sim(poissonratearrivals, totalTime, meangroupsize, meanFood, cashCard,meancash, meancard):
        customersArriving  = customer.arrive(poissonratearrivals, totalTime, meangroupsize)
        
        if simulation.modelExtension == 2: 
            customersArriving = customer.groupReduceFifteenPercent(customersArriving)
        
        customersGottenFood = customer.takeFood(meanFood, customersArriving)
        customersCashCard = customer.cardcash(cashCard, customersGottenFood)
        
        
        # Initialise
        timeCurrent = 0 #start at t=0
        amountOfQueues = 3
        queues = [[] for i in range(amountOfQueues)]
        timeFinished = [[] for i in range(amountOfQueues)]
        finishedCustomers = zeros(amountOfQueues)
        
        customerInfoSortqueue = sorted(customersCashCard.items(),key=lambda item: (item[1][3]))
        
            
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
            customerInfoIndiv, queues = service.assignToQueueIndiv(queues, customerInfoSortqueue[i])
            
            # Calculate the waiting time for the customer
            customerInfoIndiv = service.waitQueue(queues,customerInfoIndiv,timeFinished)

                        
            # Calculate the service time for the customer
            customerInfoIndiv = service.servicetimeIndiv(meancash, meancard,customerInfoIndiv)

            
            # Calculate the time a customer is finished
            customerInfoIndiv, TimeFinished = service.finish(customerInfoIndiv, timeFinished)

            listAll.append(customerInfoIndiv)
        timeEndEmptyQueue = [max(timeFinished[i]) for i in range(amountOfQueues)]
        timeEndEmptyQueues = max(timeEndEmptyQueue)

        return timeEndEmptyQueues, listAll
    
    
    def results(sim):
        groupNr = 0
        arrTime = 1
        timeFood = 2
        timeQueue = 3
        cashCard = 4
        nrQueue = 5
        waitTime = 6
        serviceTime = 7
        finishTime = 8
   
        
        # Question 1
        print("Question 1 ")
        # Sojourn time arbitrary customer (individual)
        i = random.randint(0,len(sim[1]))
        sojournTime = sim[1][i][1][finishTime] - sim[1][i][1][arrTime]
         
        sojournTimeIndividual = []
        for i in range(len(sim[1])):
            sojournTimeIndividual.append(sim[1][i][1][finishTime] - sim[1][i][1][arrTime])
        plt.hist(sojournTimeIndividual, bins =15)
        plt.show()
        
        # Expected time spend waiting in queue
        queueTimeList = []
        for i in range(len(sim[1])):
            queueTimeList.append(sim[1][i][1][waitTime])
        print("mean waiting time", mean(queueTimeList))
        print("std waiting time", std(queueTimeList))
        
        # Expected number customers in the canteen        
        CustomersInCanteenSeconds = [0 for i in range(int(simulation.totalTime))] 
        for i in range(len(sim[1])): 
            j = 0
            for j in range(int(sim[1][i][1][arrTime]), int(sim[1][i][1][finishTime])): #change if stepsize is smaller than 1 seconde 
                if 0<j <simulation.totalTime:
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
            Group = sim[1][i][1][groupNr]
            if Group not in allGroups:
                allGroups.append(Group)
        dictGroups = {}

        for i in allGroups:
            ALLTIME = []
            for g in range(len(sim[1])):
                G = sim[1][g][1][groupNr]
                if G == i:
                    arrivalTime = sim[1][g][1][arrTime]
                    ALLTIME.append(sim[1][g][1][finishTime])
                    maxTime = max(ALLTIME)
                dictGroups[i] = (arrivalTime, maxTime)
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
        lb1 = mean(sojournTimeIndividual) - 1.96*sqrt(var(sojournTimeIndividual)/len(sim[1]))
        ub1 = mean(sojournTimeIndividual) + 1.96*sqrt(var(sojournTimeIndividual)/len(sim[1]))
        print("Half-width arbitrary customer", 1.96*sqrt(var(sojournTimeIndividual)/len(sim[1])))
        print("Confidence interval arbitrary customer", lb1, ",", ub1)
        
        # arbitrary group
        lb1 = mean(sojournGroup) - 1.96*sqrt(var(sojournGroup)/len(allGroups))
        ub1 = mean(sojournGroup) + 1.96*sqrt(var(sojournGroup)/len(allGroups))
        print("Half-width arbitrary customer", 1.96*sqrt(var(sojournGroup)/len(allGroups)))
        print("Confidence interval arbitrary customer", lb1, ",", ub1)
        return "finished Simulation"
        
        
    def question3(numberOfRepeats):  
        arrTime = 1
        finishTime = 8
        listAll = []
        for i in range(numberOfRepeats):
            sim = simulation.sim(simulation.poissonratearrivals, simulation.totalTime, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
            customersInCanteenSeconds = [0 for i in range(int(simulation.totalTime))] 
            for i in range(len(sim[1])): 
                for j in range(int(sim[1][i][1][arrTime]), int(sim[1][i][1][finishTime])): #change if stepsize is smaller than 1 seconde 
                    if 0 < j < simulation.totalTime:
                        customersInCanteenSeconds[j] += 1
            listAll.append(customersInCanteenSeconds) 
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
              
sim = simulation.sim(simulation.poissonratearrivals, simulation.totalTime, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
all_results = simulation.results(sim) 
question3 = simulation.question3(50)    
