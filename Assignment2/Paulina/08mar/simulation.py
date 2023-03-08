from service import service
from customer import customer
from numpy import zeros, mean, random, std, linspace
import time
import matplotlib.pyplot as plt

class simulation:
    # simulate use cases
    # for 1 hour: 12.00h-13.00h

    poissonratearrivals = 60 #TODO in minutes make sure that the units are everwhere the same  
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
        
        customer_info_sortqueue = sorted(CustomersCashCard.items(),key=lambda item: (item[1][2]))
        
        listAll = []
        # print("Customers sorted by queueing time", customer_info_sortqueue)
        for i in range(len(customer_info_sortqueue)):
            # Set new time to time a customer arrives at the queues
            TimeToQueue = customer_info_sortqueue[i][1][2]
            if TimeCurrent <= TimeToQueue:
                TimeCurrent = TimeToQueue
            # print("1. TimeCurrent = ", TimeCurrent, "indiv_customer =" ,customer_info_sortqueue[i])
            # print("1. TimeCurrent = ", TimeCurrent)
            # print("indiv_customer =" ,customer_info_sortqueue[i])
            # print("   ")
            
            # Update the queues: check for each queue if people left the queue before the current time
            for j in range(len(Queues)):
                FinishedCustomers[j],Queues[j] = service.remove_from_queue(TimeCurrent, TimeFinished[j], FinishedCustomers[j], Queues[j])
            # print("2. Queues = ", Queues, "Finished customers = ",FinishedCustomers)
            # print("2. Queues = ", Queues)
            # print("Finished customers = ",FinishedCustomers)
            # print("   ")
            
            # Assign the customer to the shortest queue
            customer_info_indiv, Queues = service.assign_to_queue_indiv(Queues, customer_info_sortqueue[i])
            # print("3. Queues = ", Queues, "customer_info_indiv ([4]=queue) = ",customer_info_indiv)
            # print("3. Queues = ", Queues)
            # print("customer_info_indiv ([4]=queue) = ",customer_info_indiv)
            # print("   ")
            
            # Calculate the waiting time for the customer
            customer_info_indiv = service.wait_queue(Queues,customer_info_indiv,TimeFinished)
            # print("5. customer_info_indiv ([6]=waittime) = ",customer_info_indiv)
            # print("   ")
                        
            # Calculate the service time for the customer
            customer_info_indiv = service.servicetime_indiv(meancash, meancard,customer_info_indiv)
            # print("4. customer_info_indiv ([5]=servicetime) = ",customer_info_indiv)
            # print("   ")
            
            # Calculate the time a customer is finished
            customer_info_indiv, TimeFinished = service.finish(customer_info_indiv, TimeFinished)
            # print("6. customer_info_indiv ([7]=finished) = ",customer_info_indiv)
            # # print("TimeFinished = ", TimeFinished)
            # print("   ")
            listAll.append(customer_info_indiv)
        TimeEndEmptyQueue = [max(TimeFinished[i]) for i in range(amount_of_queues)]
        TimeEndEmptyQueues = max(TimeEndEmptyQueue)
        # for i in range(len(listAll)):
        #     print("ListAll", listAll[1][i][1])
        #print("listAll", listAll)
        return TimeEndEmptyQueues, listAll
    
    
    def results(sim):
        # Question 1
        # sojourn time arbitrary customer (individual)
        #TimeEndEmptyQueues, listAll = sim(simulation.poissonratearrivals, simulation.total_time, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
        i = random.randint(0,len(sim[1]))
        print("arrival", sim[1][i][1][0])
        print("departure", sim[1][i][1][-1])
        sojourn_time = sim[1][i][1][-1] - sim[1][i][1][0]
        print("sojourn time 1 customer", i, sojourn_time)
         
        sojourn_time_individual = []
        for i in range(len(sim[1])):
            sojourn_time_individual.append(sim[1][i][1][-1]  - sim[1][i][1][0])
        # print(sojourn_time_individual)
        #plt.plot(sojourn_time_individual, "x")
        #plt.hist(sojourn_time_individual, bins =15)
        #plt.show()
        print(mean(sojourn_time_individual))
        print(std(sojourn_time_individual))
        
        
        
        
        
        # Question 3
        # give distribution number customers present in canteen: average, std, histogram
        #PeopleInCanteen = zeros(4000) # in size when the latetes customers leave 
        PeopleInCanteen = []
        print(sim[1][1], int(sim[1][i][0]), sim[1][i][0])
        for j in range(int(sim[1][0][1][0]), int(sim[1][0][1][-1])): #change if stepsize is smaller than 1 seconde 
                print(j) 
        for i in range(len(sim[1])): 
            for j in range(int(sim[1][i][1][0]), int(sim[1][i][1][-1])): #change if stepsize is smaller than 1 seconde 
                PeopleInCanteen.append(j)
        AveragePeopleInCanteen = mean(PeopleInCanteen)
        StandardDeviationPeopleInCanteen = std(PeopleInCanteen)
        
        print("############################################################################")
        print("                                 Question 3                                 ") 
        print("############################################################################")
        print("People in the Canteen, each minute: ", PeopleInCanteen)
        print("Average of People in the Canteen, each minute:", AveragePeopleInCanteen)
        print("Standard deviation people in canteen:", StandardDeviationPeopleInCanteen)
        plt.hist(PeopleInCanteen, bins = 60)
        plt.title("People in the Canteen for "+ r'$\lambda$ ='+ str(round(simulation.poissonratearrivals/60))+ " min")
        plt.ylabel("People in the canteen")
        plt.xlabel("Time people are in the canteen, given in Minutes")
        x = linspace(0,60,6)
        xlocation = linspace(0,3600,6)
        plt.xticks(ticks = xlocation, labels = x)
        plt.show()
                    
        
    
    
    
# customer_info_sortqueue = simulation.sim(120, 500, 5, 80, 0.4, 15, 20)
# start = time.time
#customer_info_sortqueue = simulation.sim(simulation.poissonratearrivals, simulation.total_time, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
# print(customer_info_sortqueue)
sim = simulation.sim(simulation.poissonratearrivals, simulation.total_time, simulation.meangroupsize, simulation.meanfood, simulation.cashCard, simulation.meancash, simulation.meancard)
all_results = simulation.results(sim)
# end = time.time
# print("start", start, "end", end)
# print("total time", end - start)
#(poissonratearrivals, totalTime, meangroupsize, meanFood, cashCard,meancash, meancard):




# =============================================================================
#     def results(self, meangroupsize, poissonratearrivals, meanfood,total_nr_queues,list_queued_customers_old):
#         # Question 1
#         # sojourn time arbitrary customer (individual)
#         i = random.randint(0,len(customer.ustomers))
#         sojourn_time = customer.Customers[i][-1] - customer.Customers[i][0]
#         
#         sojourn_time_individual = []
#         for i in range(len(customer.Customers)):
#             sojourn_time_individual.append(customer.Customers[i][-1] - customer.Customers[i][0])
#         print(mean(sojourn_time_individual))
#         print(std(sojourn_time_individual))
#                                      
#         # expected time spend waiting in queue
#         queue_time_list = []
#         index_start_queue = 4
#         index_end_queue = 5
#         for i in range(len(customer.Customers)):
#             queue_time_list.append(customer.Customers[i][index_end_queue] - customer.Customers[i][index_start_queue])
#         print(mean(queue_time_list))
#         print(std(queue_time_list))
#         
#         # expected number customers in the canteen
#         
#         
#         
#         # Question 2
#         # sojourn time group
#         sojourn_time_group = []
#         for i in range(len(customer.Customers)):
#             sojourn_time_group.append(customer.Customers[i][-1] - customer.Customers[i][0])
#         print(mean(sojourn_time_group))
#         print(std(sojourn_time_group))
#         
#         
#         # Question 3
#         # give distribution number customers present in canteen: average, std, histogram
#         for i in range(len(listAll): 

#         
#         
#         # Question 4
#         # 95% confidence intervals mean sojourn time individual and per group
#         
#         
#         # listofarrivals, groupnumber, individualnumber = arrive(meangroupsize, poissonratearrivals)
#         # time_customer_arrives_at_queue, list_time_it_takes_to_get_food_per_individual = take_food(meanfood)
#         # queue, list_queued_customers_new = assign_to_queue(total_nr_queues, time_customer_arrives_at_queue, list_queued_customers_old)
#         # if queue > 1:
#         #       servicetime = service(meancash, meancard, cashpercentage)
#         # 
# 
# 
# 
# s = simulation()
# print(simulation.results(3, 2, 3, 3, zeros(3)))
# =============================================================================