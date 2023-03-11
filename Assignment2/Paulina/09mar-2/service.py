from customer import customer
from numpy import argmin, random, zeros 

class service:
    # This class determines the service times, which are exponentially distributed
    # with means 20 and 12 seconds for payment by cash and card, respectively. It has
    # been observed that 40 % of customers pay cash.
    # 3 cashiers
    
    groupNr = 0
    arrTime = 1
    timeFood = 2
    timeQueue = 3
    cashCard = 4
    nrQueue = 5
    waitTime = 6
    serviceTime = 7
    finishTime = 8
    
    # an individual is assigned to the shortest queue
    def assignToQueueIndiv(queueInfo, customerInfoIndiv):
        MinQueues = [i for i in range(len(queueInfo)) if queueInfo[i] == min(queueInfo)]
        queue = random.choice(MinQueues)
        customerInfoIndiv[1].append(queue)
        queueInfo[queue].append(customerInfoIndiv[0])
        return customerInfoIndiv, queueInfo

    # Calculate the service time for an individual
    def servicetimeIndiv(meancash, meancard,customerInfoIndiv):
        if customerInfoIndiv[1][service.cashCard] == "cash":
            servicetime = random.exponential(meancash) #servicetime cash
        elif customerInfoIndiv[1][service.cashCard] == "card":
            servicetime = random.exponential(meancard) #servicetime card
        else:
            print("card/cash not defined well")
        customerInfoIndiv[1].append(servicetime)
        return customerInfoIndiv   

    # Calculate the waiting time for an individual
    def waitQueue(queueInfo, customerInfoIndiv, timeLastPayment):#init time_last_payment as zeros(len(queues))
        queue = customerInfoIndiv[1][service.nrQueue]
        if len(queueInfo[queue]) == 1: #you are the only customer in the queue
            waittime = 0
        else:
            waittime = timeLastPayment[queue][-1] - customerInfoIndiv[1][service.timeQueue]
        customerInfoIndiv[1].append(waittime)
        return customerInfoIndiv
    
    # Calculate the finishtime for an individual
    def finish(customerInfoIndiv, timeLastPayment): 
        queue = customerInfoIndiv[1][service.nrQueue]
        serviceTime = customerInfoIndiv[1][service.serviceTime]
        waitTime = customerInfoIndiv[1][service.waitTime]
        tFinished = customerInfoIndiv[1][service.timeQueue] + waitTime + serviceTime #tqueue + waittime + servicetime
        timeLastPayment[queue].append(tFinished)
        customerInfoIndiv[1].append(tFinished)
        return customerInfoIndiv, timeLastPayment
    
    # Check if people left the queue and update the queue
    def removeFromQueue(currentTime, timeLastPaymentQueue, alreadyFinishedJobs, queueInfoQueue):
        finishedJobs = [i for i in timeLastPaymentQueue if i <= currentTime]
        amountFinishedJobs = len(finishedJobs)
        newlyFinishedJobs = int(amountFinishedJobs - alreadyFinishedJobs)
        alreadyFinishedJobs = amountFinishedJobs
        queueInfoQueue = queueInfoQueue[newlyFinishedJobs:]
        return amountFinishedJobs,queueInfoQueue
