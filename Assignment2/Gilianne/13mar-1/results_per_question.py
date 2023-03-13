### Results per question

from customer import customer
from service import service
from simulation import simulation
from numpy import zeros, mean, random, std, sqrt, var, linspace, array
#from numpy.ndarray import flatten
import time
import matplotlib.pyplot as plt


class results:
    
    extension = 0
    poissonratearrivals = 4
    meangroupsize = 3
    meanFood = 80 #seconds
    totalNrQueues = 3
    # listQueuedCustomersOld = zeros(totalNrQueues)
    totalTime = 3600 # in seconds 
    cashpayments = 0.4    # 0.4 for basic, 0 for extension 3
    meancard = 12
    meancash = 20
    
    #Index
    groupNr = 0
    arrTime = 1
    timeFood = 2
    timeQueue = 3
    cashCard = 4
    nrQueue = 5
    waitTime = 6
    serviceTime = 7
    finishTime = 8
    
    
    def Question1(nrRuns):
        
        Q1MeanSojourn = []
        Q1StdSojourn = []
        Q1MeanQueue0 = []
        Q1StdQueue0 = []
        Q1MeanQueue1 = []
        Q1StdQueue1 = []
        Q1MeanQueue2 = []
        Q1StdQueue2 = []
        Q1MeanNrCustomer = []
        Q1StdNrCustomer = []
        
        for i in range(nrRuns):
            sim = simulation.sim(results.extension, results.poissonratearrivals, results.totalTime, results.meangroupsize, results.meanFood, results.cashpayments, results.meancash, results.meancard)
    
            # Sojourn time arbitrary customer (individual)            
            sojournTimeIndividual = []
            for i in range(len(sim[1])):
                sojournTimeIndividual.append(sim[1][i][1][results.finishTime] - sim[1][i][1][results.arrTime])
            meanQ1Sojourn = mean(sojournTimeIndividual)
            stdvQ1Sojourn = std(sojournTimeIndividual)
            Q1MeanSojourn.append(meanQ1Sojourn)
            Q1StdSojourn.append(stdvQ1Sojourn)
            

            # Expected time spend waiting in queue
            queueTimeList0 = []
            queueTimeList1 = []
            queueTimeList2 = []
            for i in range(len(sim[1])):
                if sim[1][i][1][results.nrQueue] == 0:
                    queueTimeList0.append(sim[1][i][1][results.waitTime])
                if sim[1][i][1][results.nrQueue] == 1:
                    queueTimeList1.append(sim[1][i][1][results.waitTime])
                if sim[1][i][1][results.nrQueue] == 2:
                    queueTimeList2.append(sim[1][i][1][results.waitTime])
            meanQ1Waiting0 = mean(queueTimeList0)
            stdQ1Waiting0 = std(queueTimeList0)
            # print(meanQ1Waiting0)
            Q1MeanQueue0.append(meanQ1Waiting0)
            Q1StdQueue0.append(stdQ1Waiting0)
            
            meanQ1Waiting1 = mean(queueTimeList1)
            stdQ1Waiting1 = std(queueTimeList1)
            Q1MeanQueue1.append(meanQ1Waiting1)
            Q1StdQueue1.append(stdQ1Waiting1)
            
            meanQ1Waiting2 = mean(queueTimeList2)
            stdQ1Waiting2 = std(queueTimeList2)
            Q1MeanQueue2.append(meanQ1Waiting2)
            Q1StdQueue2.append(stdQ1Waiting2)
            
            # Expected number customers in the canteen        
            CustomersInCanteenSeconds = [0 for i in range(int(results.totalTime))] 
            for i in range(len(sim[1])): 
                j = 0
                for j in range(int(sim[1][i][1][results.arrTime]), int(sim[1][i][1][results.finishTime])): #change if stepsize is smaller than 1 seconde 
                    if 0<j <results.totalTime:
                        CustomersInCanteenSeconds[j] += 1
            AverageCustomersInCanteen = mean(CustomersInCanteenSeconds)
            StandardDeviationCustomersInCanteen = std(CustomersInCanteenSeconds)
            Q1MeanNrCustomer.append(AverageCustomersInCanteen)
            Q1StdNrCustomer.append(StandardDeviationCustomersInCanteen)

        print("Question 1 ")
        print("Sojourn time")
        print("Mean sojourn time", mean(Q1MeanSojourn))
        print("Std sojourn time", std(Q1StdSojourn))
        
        # lower and upper bound for confidence interval question 4
        lb1 = mean(Q1MeanSojourn) - 1.96*sqrt(var(Q1MeanSojourn)/nrRuns)
        ub1 = mean(Q1MeanSojourn) + 1.96*sqrt(var(Q1MeanSojourn)/nrRuns)
        print("Confidence interval (Question 4)")  
        print("Half-width arbitrary customer", 1.96*sqrt(var(Q1MeanSojourn)/nrRuns))
        print("Confidence interval arbitrary customer", lb1, ",", ub1)
        
        
        print("   ")
        print("Waiting time")
        print("Average waiting time queue 0 = ", mean(Q1MeanQueue0))
        print("stdv waiting time queue 0 = ", std(Q1StdQueue0))
        print("Average waiting time queue 1 = ", mean(Q1MeanQueue1))
        print("stdv waiting time queue 1 = ", std(Q1StdQueue1))
        print("Average waiting time queue 2 = ", mean(Q1MeanQueue2))
        print("stdv waiting time queue 2 = ", std(Q1StdQueue2))
        print("  ")
        print("Number customers")
        print("Mean custumers in the canteen each second:", mean(Q1MeanNrCustomer))
        print("Standard deviation customers in canteen:", std(Q1StdNrCustomer))
        return "Question 1 finished"
    
    
    def Question2(nrRuns): 
       
        Q2MeanSojournGroup = []
        Q2StdSojournGroup = []
        
        for i in range(nrRuns):
            sim = simulation.sim(results.extension, results.poissonratearrivals, results.totalTime, results.meangroupsize, results.meanFood, results.cashpayments, results.meancash, results.meancard)
            
            allGroups = []
            for i in range(len(sim[1])):
                Group = sim[1][i][1][results.groupNr]
                if Group not in allGroups:
                    allGroups.append(Group)
            dictGroups = {}

            for i in allGroups:
                ALLTIME = []
                for g in range(len(sim[1])):
                    G = sim[1][g][1][results.groupNr]
                    if G == i:
                        arrivalTime = sim[1][g][1][results.arrTime]
                        ALLTIME.append(sim[1][g][1][results.finishTime])
                        maxTime = max(ALLTIME)
                    dictGroups[i] = (arrivalTime, maxTime)
            sojournGroup = []
            dictGroups = list(map(list, dictGroups.items()))
            for i in range(len(allGroups)):
                sojournGroup.append(dictGroups[i][1][1] - dictGroups[i][1][0])
                
            Q2MeanSojournGroup.append(mean(sojournGroup))
            Q2StdSojournGroup.append(std(sojournGroup))
            
        print("Question 2")
        print("Mean sojourn time per group", mean(Q2MeanSojournGroup))
        print("Std sojourn time per group", std(Q2StdSojournGroup))
        print(" ")
        # Confidence intervals question 4
        print("Confidence interval (Question 4)")  
        lb1 = mean(Q2MeanSojournGroup) - 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns)
        ub1 = mean(Q2MeanSojournGroup) + 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns)
        print("Half-width arbitrary group", 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns))
        print("Confidence interval arbitrary group", lb1, ",", ub1) # I think this should be arbitrary group, so I changed the printed sentences customer -> group
        
        return "Question 2 finished"
        
        
    def Question3(nrRuns):
        # arrTime = 1
        # finishTime = 8
        listAll = []
        for i in range(nrRuns):
            sim = simulation.sim(results.poissonratearrivals, results.totalTime, results.meangroupsize, results.meanfood, results.cashpayments, results.meancash, results.meancard)
            customersInCanteenSeconds = [0 for i in range(int(results.totalTime))] 
            for i in range(len(sim[1])): 
                for j in range(int(sim[1][i][1][results.arrTime]), int(sim[1][i][1][results.finishTime])): #change if stepsize is smaller than 1 seconde 
                    if 0<j <results.totalTime:
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
    


# results.Question2(10)
print(results.Question1(1000))