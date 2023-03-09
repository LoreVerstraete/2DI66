from service import service
from customer import customer
from numpy import zeros, mean, random, std, sqrt, var, linspace
import time
import matplotlib.pyplot as plt

class simulation:
    # simulate use cases
    # for 1 hour: 12.00h-13.00h

    poissonratearrivals = 2 #TODO in minutes make sure that the units are everwhere the same  
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
        # print("Customers not sorted",CustomersCashCard)
        
        # Initialise
        TimeCurrent = 0 #start at t=0
        amount_of_queues = 3
        Queues = [[] for i in range(amount_of_queues)]
        TimeFinished = [[] for i in range(amount_of_queues)]
        FinishedCustomers = zeros(amount_of_queues)
        
        customer_info_sortqueue = sorted(CustomersCashCard.items(),key=lambda item: (item[1][3]))
        
        listAll = []
        # print("Customers sorted by queueing time", customer_info_sortqueue)
        for i in range(len(customer_info_sortqueue)):
            # Set new time to time a customer arrives at the queues
            TimeToQueue = customer_info_sortqueue[i][1][3]
            if TimeCurrent <= TimeToQueue:
                TimeCurrent = TimeToQueue
            # print("1. TimeCurrent = ", TimeCurrent, "indiv_customer =" ,customer_info_sortqueue[i])
            
            # Update the queues: check for each queue if people left the queue before the current time
            for j in range(len(Queues)):
                FinishedCustomers[j],Queues[j] = service.remove_from_queue(TimeCurrent, TimeFinished[j], FinishedCustomers[j], Queues[j])
            # print("2. Queues = ", Queues, "Finished customers = ",FinishedCustomers)
            
            # Assign the customer to the shortest queue
            customer_info_indiv, Queues = service.assign_to_queue_indiv(Queues, customer_info_sortqueue[i])
            # print("3. Queues = ", Queues, "customer_info_indiv ([4]=queue) = ",customer_info_indiv)
            
            # Calculate the waiting time for the customer
            customer_info_indiv = service.wait_queue(Queues,customer_info_indiv,TimeFinished)
            # print("5. customer_info_indiv ([6]=waittime) = ",customer_info_indiv)
                        
            # Calculate the service time for the customer
            customer_info_indiv = service.servicetime_indiv(meancash, meancard,customer_info_indiv)
            # print("4. customer_info_indiv ([5]=servicetime) = ",customer_info_indiv)
            
            # Calculate the time a customer is finished
            customer_info_indiv, TimeFinished = service.finish(customer_info_indiv, TimeFinished)
            # print("6. customer_info_indiv ([7]=finished) = ",customer_info_indiv)

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
        print("############################################################################")
        print("                                 Question 1                                 ") 
        print("############################################################################")
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
        # # index_start_queue = 4
        # # index_end_queue = 5
        for i in range(len(sim[1])):
            queue_time_list.append(sim[1][i][1][WaitTime])
        print(mean(queue_time_list ))
        
        # Expected number customers in the canteen
        
        
        # Question 2
        # sojourn time group
        print("############################################################################")
        print("                                 Question 2                                 ") 
        print("############################################################################")
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
            # print("find finish and start")
            sojournGroup.append(dictGroups[i+1][1] - dictGroups[i+1][0])
        print("Mean sojourn time per group", mean(sojournGroup))
        print("Std sojourn time per group", std(sojournGroup))
        
        
        # Question 3
        # give distribution number customers present in canteen: average, std, histogram
        
        
                PeopleInCanteenSeconds = zeros((int(sim[0]+1)))
        for i in range(len(sim[1])): 
            j = 0
            for j in range(int(sim[1][i][1][ArrTime]), int(sim[1][i][1][FinishTime])): #change if stepsize is smaller than 1 seconde 
                PeopleInCanteenSeconds[j] += 1
        
        PeopleInCanteenSeconds = zeros((int(sim[0]+1)))
        for i in range(len(sim[1])): 
            j = 0
            for j in range(int(sim[1][i][1][ArrTime]), int(sim[1][i][1][FinishTime])): #change if stepsize is smaller than 1 seconde 
                PeopleInCanteenSeconds[j] += 1

        print("PeopleInCanteenSeconds", PeopleInCanteenSeconds)
        AveragePeopleInCanteen = mean(PeopleInCanteenSeconds)
        StandardDeviationPeopleInCanteen = std(PeopleInCanteenSeconds)
        
        print("############################################################################")
        print("                                 Question 3                                 ") 
        print("############################################################################")
        print("Groups of people in the canteen each seconde:", AveragePeopleInCanteen )
        print("Standard deviation people in canteen:", StandardDeviationPeopleInCanteen)
        plt.hist(PeopleInCanteenSeconds,bins=20)
        plt.xlabel("Size of groups of people")
        plt.ylabel("frequence")
        plt.title("Distribution of people in the canteen")
        plt.show()
        
        
        # Question 4
        print("############################################################################")
        print("                                 Question 4                                 ") 
        print("############################################################################")
        # arbitrary customer 
        lb1 = mean(sojourn_time_individual) - 1.96*sqrt(var(sojourn_time_individual)/len(sim[1]))
        ub1 = mean(sojourn_time_individual) + 1.96*sqrt(var(sojourn_time_individual)/len(sim[1]))
        print("Half-width arbitrary customer", 1.96*sqrt(var(sojourn_time_individual)/len(sim[1])))
        print("Confidence interval arbitrary customer", lb1, ",", ub1)
        
        # arbitrary group
        lb1 = mean(sojournGroup) - 1.96*sqrt(var(sojournGroup)/len(allGroups))
        ub1 = mean(sojournGroup) + 1.96*sqrt(var(sojournGroup)/len(allGroups))
        print("Half-width arbitrary customer", 1.96*sqrt(var(sojournGroup)/len(allGroups)))
        print("Confidence interval arbitrary customer", lb1, ",", ub1)
        
    def question3(numberOfRepeats):  
        listAll = zeros((numberOfRepeats))
        for i in range(numberOfRepeats):
            sim = simulation.sim(simulation.poissonratearrivals, simulation.total_time, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
            PeopleInCanteenSeconds = np.zero(len(sim[1]))
            for i in range(len(sim[1])): 
                j = 0
                for j in range(int(sim[1][i][1][ArrTime]), int(sim[1][i][1][FinishTime])): #change if stepsize is smaller than 1 seconde 
                    PeopleInCanteenSeconds[j] += 1
            listAll.append(PeopleInCanteenSeconds)
        
#sim = simulation.sim(simulation.poissonratearrivals, simulation.total_time, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
#all_results = simulation.results(sim)  

print(simulation.question3())  