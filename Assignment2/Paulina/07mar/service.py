from customer import customer
from numpy import argmin, random, zeros 

class service:
    # This class determines the service times, which are exponentially distributed
    # with means 20 and 12 seconds for payment by cash and card, respectively. It has
    # been observed that 40 % of customers pay cash.
    # 3 cashiers
  
    def assign_to_queue(queue_info,lenqueue,customer_info): #init queue info = [[],[],[]]
        customer_info_sortqueue = sorted(customer_info.items(),key=lambda item: (item[1][2]))
        #print(customer_info_sortqueue)
        for i in range(len(customer_info_sortqueue)):
            for j in range(len(queue_info)):
                lenqueue[j] = len(queue_info[j])
            queue = argmin(lenqueue)
            #print(queue)
            customer_info_sortqueue[i][1].append(queue)
            queue_info[queue].append(customer_info_sortqueue[i][0])
        return customer_info_sortqueue, queue_info

    def service(meancash, meancard,customer_info):
            for i in range(len(customer_info)):
                if customer_info[i][1][3] == "cash":
                    servicetime = random.exponential(meancash) #servicetime cash
                if customer_info[i][1][3] == "card":
                    servicetime = random.exponential(meancard) #servicetime card
                else:
                    print("card/cash not defined well")
                customer_info[i][1].append(servicetime)
            return customer_info
        
        # first calc if it is card or cash (random 40% cash)
        # service times are exponentially distributed with means 20 for cash
        # service times are exponentially distributed with means 12 for card
        # timefinished = save time customer leaves the cashier
        # timequeued = timefinished - servicetime - que
        # list_queued_customers_old[queue] -= 1
        # list_queued_customers_new = list_queued_customers_old
        # output servicetime, list_queued_customers_new

# arrival = customer.arrive(4, 60,4)
# print(arrival)
# print(arrival[0][0])
# arrival_group = []
# for i in range(len(arrival)):
#     arrival_group.append([arrival[i][0]]*arrival[i][1])
# arrival_individual = [item for sublist in arrival_group for item in sublist]
# print(arrival_individual)

# print(argmin([3,3,3]))

# customers = customer.arrive(3, 20, 2) 
# print("arrivaltimes: ", customers, "\n")
# takenFood = customer.take_food(3, customers)
# print("time to take food", takenFood, "\n")
# CustomerInfo = customer.cardcash(0.4, takenFood) 
# print("cash or card ", CustomerInfo)
# CustomerINFO= {0: [4,1,5, 'cash'], 1: [9, 6, 15, 'card'], 2: [12, 2, 14, 'card']}
# customer_info = customer.customer_info([0,6,20,30],[10,60,30,50],0.4)
# print(CustomerINFO)
# print(CustomerINFO.items())
# sorted_customer_info = sorted(CustomerINFO.items(),key=lambda item: (item[1][2]))
# print(sorted_customer_info[1])
# print(sorted_customer_info[1][0])


#customer_info_sortqueue, queue_info = service.assign_to_queue([[],[],[]],[0,0,0],CustomerINFO)
#print(customer_info_sortqueue, queue_info)
# print(sorted_customer_info[3])
# print(customer.take_food(80, [1,2]))
# print(service.assign_to_queue([3,0,1],customer_info))