from service import service
from customer import customer
from numpy import zeros, mean, random, std

class simulation:
    # simulate use cases
    # for 1 hour: 12.00h-13.00h

    poissonratearrivals = 0.1 #TODO in minutes make sure that the units are everwhere the same  
    meangroupsize = 3
    meanfood = 80 #seconds
    total_nr_queues = 3
    list_queued_customers_old = zeros(total_nr_queues)
    total_time = 500 # in seconds 

    
    def sim(poissonratearrivals, totalTime, meangroupsize, meanFood, cashCard ):
        Customers = customer.arrive(poissonratearrivals, totalTime, meangroupsize)
        CustomersGottenFood = customer.take_food(meanFood, Customers)
        CustomersCashCard = customer.cardcash(cashCard, CustomersGottenFood)
        QueueList = [[],[],[]]
        lenqueue = zeros((len(QueueList)))
        for i in range(len(CustomersCashCard)): 
            TimeToGetToQueue = CustomersCashCard[i][1][2]
            selectedQueu = service.assign_to_queue(QueueList, lenqueue, CustomersCashCard[i])
        return CustomersCashCard

        
print(simulation.sim(6, 50, 3, 20, 0.4))
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
#         
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