from customer import customer
from service import service
from simulation import simulation
from numpy import zeros, mean, random, std, sqrt, var, linspace, array
#from numpy.ndarray import flatten
import time
import matplotlib.pyplot as plt
import numba as nb


class results:
    
    # input values
    extension = 2
    poissonratearrivals = 4
    meangroupsize = 3
    meanFood = 80 #seconds
    totalNrQueues = 3
    # listQueuedCustomersOld = zeros(totalNrQueues) # not used anymore
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
    
    #@nb.jit()
    def results(nrRuns):
        startTime = time.time()
        
        # Lists for all questions to store the mean and standard deviation per run
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
        
        Q2MeanSojournGroup = []
        Q2StdSojournGroup = []
        
        Q3listAll = []
        
        percentageExtension3 = [] 
        
        for i in range(nrRuns):
            # print("nrRun", i)
            # Run the simulation every time
            sim = simulation.sim(results.extension, results.poissonratearrivals, results.totalTime, results.meangroupsize, results.meanFood, results.cashpayments, results.meancash, results.meancard)
            
            percentageExtension3.append(sim[2])
            
            # Sojourn time arbitrary customer (individual)            
            sojournTimeIndividual = []                  # an empty list to store all times
            for i in range(len(sim[1])):
                # compute for every customer the sojourn time
                sojournTimeIndividual.append(sim[1][i][1][results.finishTime] - sim[1][i][1][results.arrTime])
            meanQ1Sojourn = mean(sojournTimeIndividual) # compute mean sojourn time
            stdvQ1Sojourn = std(sojournTimeIndividual)  # compute std sojourn time
            Q1MeanSojourn.append(meanQ1Sojourn)         # add mean time to list of means
            Q1StdSojourn.append(stdvQ1Sojourn)          # add stdv to lsit of standard deviations
            

            # Expected time spend waiting in queue
            queueTimeList0 = []                         # an empty list to store all times
            queueTimeList1 = []                         # an empty list to store all times
            queueTimeList2 = []                         # an empty list to store all times
            for i in range(len(sim[1])):
                # Per queue add the waiting time to the list
                if sim[1][i][1][results.nrQueue] == 0:
                    queueTimeList0.append(sim[1][i][1][results.waitTime])
                if sim[1][i][1][results.nrQueue] == 1:
                    queueTimeList1.append(sim[1][i][1][results.waitTime])
                if sim[1][i][1][results.nrQueue] == 2:
                    queueTimeList2.append(sim[1][i][1][results.waitTime])
            meanQ1Waiting0 = mean(queueTimeList0)       # compute mean waiting time queue 0
            stdQ1Waiting0 = std(queueTimeList0)         # compute stdv waiting time queue 0
            # print(meanQ1Waiting0)
            Q1MeanQueue0.append(meanQ1Waiting0)         # append the mean to the list of means of queue 0
            Q1StdQueue0.append(stdQ1Waiting0)           # append stdv to the list of stdv of queue 0
            
            meanQ1Waiting1 = mean(queueTimeList1)       # compute mean waiting time queue 1
            stdQ1Waiting1 = std(queueTimeList1)         # compute stdv waiting time queue 1
            Q1MeanQueue1.append(meanQ1Waiting1)         # append the mean to the list of means of queue 1
            Q1StdQueue1.append(stdQ1Waiting1)           # append stdv to the list of stdv of queue 1
            
            meanQ1Waiting2 = mean(queueTimeList2)       # compute mean waiting time queue 2
            stdQ1Waiting2 = std(queueTimeList2)         # compute stdv waiting time queue 2
            Q1MeanQueue2.append(meanQ1Waiting2)         # append the mean to the list of means of queue 2
            Q1StdQueue2.append(stdQ1Waiting2)           # append the stdv the list of stdv of queue 2
            
            # Expected number customers in the canteen  
            # Create list of zeros for all seconds per run
            CustomersInCanteenSeconds = [0 for i in range(int(results.totalTime))] 
            for i in range(len(sim[1])): 
                j = 0
                for j in range(int(sim[1][i][1][results.arrTime]), int(sim[1][i][1][results.finishTime])): #change if stepsize is smaller than 1 seconde 
                    if 0<j <results.totalTime:
                        CustomersInCanteenSeconds[j] += 1
                    
            AverageCustomersInCanteen = mean(CustomersInCanteenSeconds)          # compute mean number customers
            StandardDeviationCustomersInCanteen = std(CustomersInCanteenSeconds) # compute stdv number customers
            Q1MeanNrCustomer.append(AverageCustomersInCanteen)                   # append mean to list of means nr customers
            Q1StdNrCustomer.append(StandardDeviationCustomersInCanteen)          # append stdv to list of stdv nr customers
            
            
            #question 2
            allGroups = []                                  # create an empty list to store all groups
            # look for each group number and append it to the list if it is not already in it
            for i in range(len(sim[1])):
                Group = sim[1][i][1][results.groupNr]
                if Group not in allGroups:
                    allGroups.append(Group)
            
            dictGroups = {} # create a dictionary with key=groupsnr and value=sojourntime of a group
            for i in allGroups:
                ALLTIME = []
                for g in range(len(sim[1])):
                    G = sim[1][g][1][results.groupNr]
                    if G == i:
                        arrivalTime = sim[1][g][1][results.arrTime]         # the arrival time is the same for all customers within a group
                        ALLTIME.append(sim[1][g][1][results.finishTime])    # append finish times for all customers within that group
                        maxTime = max(ALLTIME)                              # determine the latest finishing time
                    dictGroups[i] = (arrivalTime, maxTime)                  # add to the dictionary the arrival time and latest finishing time
            sojournGroup = []  # create an empty list to store the sojourn times per group
            dictGroups = list(map(list, dictGroups.items()))
            for i in range(len(allGroups)):
                # for all groups compute the sojourn time and append to the list of sojourn times
                sojournGroup.append(dictGroups[i][1][1] - dictGroups[i][1][0])
                
            Q2MeanSojournGroup.append(mean(sojournGroup))       # compute mean sojourn time and append to list of mean sojourn times per run
            Q2StdSojournGroup.append(std(sojournGroup))         # compute stdv sojourn time and append to list of stdv sojourn times per run
            
            # Question 3
            # make one list with number of customers in the canteen of all runs
            customersInCanteenSeconds = [0 for i in range(int(results.totalTime))] 
            for i in range(len(sim[1])): 
                for j in range(int(sim[1][i][1][results.arrTime]), int(sim[1][i][1][results.finishTime])): #change if stepsize is smaller than 1 seconde 
                    if 0<j <results.totalTime:
                        customersInCanteenSeconds[j] += 1
            Q3listAll.append(customersInCanteenSeconds) 
            
            
           
        print("extension", results.extension, "poisson rate", results.poissonratearrivals)
            
        print("Question 1 ")
        print("Sojourn time")
        print("Mean of mean sojourn time", mean(Q1MeanSojourn))
        # print("Stdv of mean sojourn time", std(Q1MeanSojourn))
        lb1 = mean(Q1MeanSojourn) - 1.96*sqrt(var(Q1MeanSojourn)/nrRuns)
        ub1 = mean(Q1MeanSojourn) + 1.96*sqrt(var(Q1MeanSojourn)/nrRuns)
        print("Half-width mean sojourn time", 1.96*sqrt(var(Q1MeanSojourn)/nrRuns))
        print("Confidence interval mean sojourn time", lb1, ",", ub1)
        print("Std sojourn time", mean(Q1StdSojourn))
        
        print("   ")
        print("Waiting time queue 0")
        print("Average waiting time queue 0 = ", mean(Q1MeanQueue0))
        print("stdv of mean waiting time", std(Q1MeanQueue0))
        lb1 = mean(Q1MeanQueue0) - 1.96*sqrt(var(Q1MeanQueue0)/nrRuns)
        ub1 = mean(Q1MeanQueue0) + 1.96*sqrt(var(Q1MeanQueue0)/nrRuns)
        print("Half-width average waiting time queue 0", 1.96*sqrt(var(Q1MeanQueue0)/nrRuns))
        print("Confidence interval average waiting time queue 0", lb1, ",", ub1)
        print("stdv waiting time queue 0 = ", mean(Q1StdQueue0))

        print("   ")
        print("Waiting time queue 1")
        print("Average waiting time queue 1 = ", mean(Q1MeanQueue1))
        print("std of mean waiting time queue 1 = ", std(Q1MeanQueue1))
        lb1 = mean(Q1MeanQueue1) - 1.96*sqrt(var(Q1MeanQueue1)/nrRuns)
        ub1 = mean(Q1MeanQueue1) + 1.96*sqrt(var(Q1MeanQueue1)/nrRuns)
        print("Half-width average waiting time queue 1", 1.96*sqrt(var(Q1MeanQueue1)/nrRuns))
        print("Confidence interval average waiting time queue 1", lb1, ",", ub1)
        print("stdv waiting time queue 1 = ", mean(Q1StdQueue1))
        
        print("   ")
        print("Waiting time queue 2")
        print("Average waiting time queue 2 = ", mean(Q1MeanQueue2))
        print("std mean waiting time queue 2 = ", std(Q1MeanQueue2))
        lb1 = mean(Q1MeanQueue2) - 1.96*sqrt(var(Q1MeanQueue2)/nrRuns)
        ub1 = mean(Q1MeanQueue2) + 1.96*sqrt(var(Q1MeanQueue2)/nrRuns)
        print("Half-width average waiting time queue 2", 1.96*sqrt(var(Q1MeanQueue2)/nrRuns))
        print("Confidence interval average waiting time queue 2", lb1, ",", ub1) 
        print("stdv waiting time queue 2 = ", mean(Q1StdQueue2))

        print("  ")
        print("Number customers")
        print("Mean custumers in the canteen each second:", mean(Q1MeanNrCustomer))
        print("std mean custumers in the canteen each second:", std(Q1MeanNrCustomer))
        lb1 = mean(Q1MeanNrCustomer) - 1.96*sqrt(var(Q1MeanNrCustomer)/nrRuns)
        ub1 = mean(Q1MeanNrCustomer) + 1.96*sqrt(var(Q1MeanNrCustomer)/nrRuns)
        print("Half-width mean custumers in the canteen each second", 1.96*sqrt(var(Q1MeanNrCustomer)/nrRuns))
        print("Confidence interval mean custumers in the canteen each second", lb1, ",", ub1)
        print("Standard deviation customers in canteen:", mean(Q1StdNrCustomer))
        
        print("  ")
        print("Question 2")
        print("Mean sojourn time per group", mean(Q2MeanSojournGroup))
        print("Std mean sojourn time per group", std(Q2MeanSojournGroup))
        lb1 = mean(Q2MeanSojournGroup) - 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns)
        ub1 = mean(Q2MeanSojournGroup) + 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns)
        print("Half-width mean sojourn time per group", 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns))
        print("Confidence interval mean sojourn time per group", lb1, ",", ub1)
        print("Std sojourn time per group", mean(Q2StdSojournGroup))
        print(" ")

        
        # Question 3
        Q3listAllarray = array(Q3listAll)
        Q3listAllFlatten = Q3listAllarray.flatten()
        plt.hist(Q3listAllFlatten, bins= 40)
        plt.xlabel('Number of customers')
        plt.ylabel('Frequency')
        #plt.xlim(0,250) # add to create histograms with the same x-axis
        plt.title('Number of customers in canteen per second')
        plt.show()
        Mean = mean(Q3listAllFlatten) 
        StandardDeviation = std(Q3listAllFlatten)
        print("Question 3")
        print("Mean:", Mean)
        print("Standard deviation:", StandardDeviation)
        
        
# =============================================================================
#         # Question 4
#         print("Question 4")  
#         # Confidence interval individual customer
#         lb1 = mean(Q1MeanSojourn) - 1.96*sqrt(var(Q1MeanSojourn)/nrRuns)
#         ub1 = mean(Q1MeanSojourn) + 1.96*sqrt(var(Q1MeanSojourn)/nrRuns)
#         print("Half-width arbitrary customer", 1.96*sqrt(var(Q1MeanSojourn)/nrRuns))
#         print("Confidence interval arbitrary customer", lb1, ",", ub1)
#         # Confidence interval customer group
#         lb1 = mean(Q2MeanSojournGroup) - 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns)
#         ub1 = mean(Q2MeanSojournGroup) + 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns)
#         print("Half-width arbitrary group", 1.96*sqrt(var(Q2MeanSojournGroup)/nrRuns))
#         print("Confidence interval arbitrary group", lb1, ",", ub1) # I think this should be arbitrary group, so I changed the printed sentences customer -> group
# =============================================================================
        
        
        #ModelExtension 2:
        if results.extension ==2: 
            print("Percentage of groups that are going to the food card: ",mean(percentageExtension3))
        
        totalTime = time.time() - startTime
        
        print("Total time", totalTime)
        return "Total time", totalTime
    
       


# results.Question2(10)
results.results(5000)



