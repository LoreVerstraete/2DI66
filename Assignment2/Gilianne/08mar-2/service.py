from customer import customer
from numpy import argmin, random, zeros 

class service:
    # This class determines the service times, which are exponentially distributed
    # with means 20 and 12 seconds for payment by cash and card, respectively. It has
    # been observed that 40 % of customers pay cash.
    # 3 cashiers

    # an individual is assigned to the shortest queue
    def assign_to_queue_indiv(queue_info,customer_info_indiv): #init queue info = [[],[],[]]
        queue = argmin([len(queue_info[i]) for i in range(len(queue_info))])
        customer_info_indiv[1].append(queue)
        queue_info[queue].append(customer_info_indiv[0])
        return customer_info_indiv, queue_info

    # Calculate the service time for an individual
    def servicetime_indiv(meancash, meancard,customer_info_indiv):
        if customer_info_indiv[1][3] == "cash":
            servicetime = random.exponential(meancash) #servicetime cash
        elif customer_info_indiv[1][3] == "card":
            servicetime = random.exponential(meancard) #servicetime card
        else:
            print("card/cash not defined well")
        customer_info_indiv[1].append(servicetime)
        return customer_info_indiv   

    # Calculate the waiting time for an individual
    def wait_queue(queue_info,customer_info_indiv,time_last_payment):#init time_last_payment as zeros(len(queues))
        queue = customer_info_indiv[1][4]
        if len(queue_info[queue]) == 1: #you are the only customer in the queue
            waittime = 0
        else:
            waittime = time_last_payment[queue][-1] - customer_info_indiv[1][2]
        customer_info_indiv[1].append(waittime)
        return customer_info_indiv
    
    # Calculate the finishtime for an individual
    def finish(customer_info_indiv, time_last_payment): 
        queue = customer_info_indiv[1][4]
        servicetime = customer_info_indiv[1][5]
        waittime = customer_info_indiv[1][6]
        t_finished = customer_info_indiv[1][2] + waittime + servicetime #tqueue + waittime + servicetime
        time_last_payment[queue].append(t_finished)
        customer_info_indiv[1].append(t_finished)
        return customer_info_indiv, time_last_payment
    
    # Check if people left the queue and update the queue
    def remove_from_queue(current_time, time_last_payment_queue, alreadyfinishedjobs, queue_info_queue):
        finishedjobs = [i for i in time_last_payment_queue if i <= current_time]
        amountfinishedjobs = len(finishedjobs)
        newlyfinishedjobs = int(amountfinishedjobs - alreadyfinishedjobs)
        alreadyfinishedjobs = amountfinishedjobs
        queue_info_queue = queue_info_queue[newlyfinishedjobs:]
        return amountfinishedjobs,queue_info_queue


# CustomerINFO= {0: [4,1,5, 'cash'], 1: [9, 6, 15, 'card'], 2: [12, 2, 14, 'card']}
# sorted_customer_info = sorted(CustomerINFO.items(),key=lambda item: (item[1][2]))
# customer_info_indiv = sorted_customer_info[1]

