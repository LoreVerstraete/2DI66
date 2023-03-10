from customer import customer
from numpy import argmin, random, zeros 

class service:
    '''
    This class determines the service, which includes the queueing process
    '''
    groupNr = 0
    arrTime = 1
    timeFood = 2
    timeQueue = 3
    cashCard = 4
    nrQueue = 5
    waitTime = 6
    serviceTime = 7
    finishTime = 8
    
    def assignToQueue(queueInfo, customerInfoIndiv):
        '''
        Assigns a customer to shortest queue
        param queueInfo: list with a list per queue within which gives the customernumbers that are in the queue
        param customerInfoIndiv: info of the customer which have the customer number and list of group number, arrival time, taking food time, arriving time at queue and payment method
        returns: the customerinfo with the shortest queue added and the queueinfo with the customer added to the shortest queue
        '''
        MinQueues = [i for i in range(len(queueInfo)) if len(queueInfo[i]) == min(len(queueInfo[j]) for j in range(len(queueInfo)))]
        queue = random.choice(MinQueues) # if multiple queues are the shortest, pick random one
        customerInfoIndiv[1].append(queue)
        queueInfo[queue].append(customerInfoIndiv[0])
        return customerInfoIndiv, queueInfo
    
    def waitQueue(queueInfo, customerInfoIndiv, timePayment):
        '''
        Calculate the waiting time for a customer
        param queueInfo: list with a list per queue within which gives the customernumbers that are in the queue
        param customerInfoIndiv: info of the customer which have the customer number and list of group number, arrival time, taking food time, arriving time at queue, payment method and queue number
        param timePayment:
        returns:customerInfoIndiv with the waitingtime added
        '''
        queue = customerInfoIndiv[1][service.nrQueue]
        if len(queueInfo[queue]) == 1: # only one customer in the queue, so no waiting time
            waittime = 0
        else:
            waittime = timePayment[queue][-1] - customerInfoIndiv[1][service.timeQueue]
        customerInfoIndiv[1].append(waittime)
        return customerInfoIndiv
    
    def servicetime(meancash, meancard,customerInfoIndiv):
        '''
        Calculate the service time for a customer
        param meancash: mean time for cash payments
        param meancard: mean time for card payments
        param customerInfoIndiv: info of the customer which have the customer number and list of group number, arrival time, taking food time, arriving time at queue, payment method, queue number and waitingtime
        returns: the customerinfo with the servicetime added
        '''
        if customerInfoIndiv[1][service.cashCard] == "cash":
            servicetime = random.exponential(meancash) #servicetime cash
        elif customerInfoIndiv[1][service.cashCard] == "card":
            servicetime = random.exponential(meancard) #servicetime card
        else:
            print("card/cash not defined well")
        customerInfoIndiv[1].append(servicetime)
        return customerInfoIndiv   

    def finish(customerInfoIndiv, timePayment): 
        '''
        Calculate the time a customer is finished
        param customerInfoIndiv: info of the customer which have the customer number and list of group number, arrival time, taking food time, arriving time at queue, payment method, queue number, waitingtime and servicetime
        param timePayment: list with a list per queue within which gives the time each customer of that queue is finished
        returns: the customerinfo with the finishing time added
        '''
        queue = customerInfoIndiv[1][service.nrQueue]
        serviceTime = customerInfoIndiv[1][service.serviceTime]
        waitTime = customerInfoIndiv[1][service.waitTime]
        timeFinished = customerInfoIndiv[1][service.timeQueue] + waitTime + serviceTime
        timePayment[queue].append(timeFinished)
        customerInfoIndiv[1].append(timeFinished)
        return customerInfoIndiv, timePayment
    
    def removeFromQueue(currentTime, timePaymentQueue, alreadyFinishedJobs, queueInfoQueue):
        '''
        Remove the finished customers from the queue
        param currentTime: time for which queue should be updated
        param timePaymentQueue: list per queue which gives the time each customer of that queue is finished
        param alreadyFinishedJobs: amount of finished customers queue already had
        param queueInfoQueue: list per queue which gives the time each customer of that queue is finished
        returns: the amountFinishedJobs and the updated queueInfoQueue
        '''
        finishedJobs = [time for time in timePaymentQueue if time <= currentTime]
        amountFinishedJobs = len(finishedJobs)
        newlyFinishedJobs = int(amountFinishedJobs - alreadyFinishedJobs) 
        alreadyFinishedJobs = amountFinishedJobs
        queueInfoQueue = queueInfoQueue[newlyFinishedJobs:] # remove the newly finished customers from the list
        return amountFinishedJobs,queueInfoQueue
