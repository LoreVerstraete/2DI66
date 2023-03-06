from customer import customer
from numpy import argmin, random

class service:
    # This class determines the service times, which are exponentially distributed
    # with means 20 and 12 seconds for payment by cash and card, respectively. It has
    # been observed that 40 % of customers pay cash.
    # 3 cashiers
        
    def assign_to_queue(list_queued_customers,customer_info):
        customer_info_sortfood = sorted(customer_info.items(),key=lambda item: (item[1]['t_foodtaken']))
        queue = argmin(list_queued_customers)
        list_queued_customers[queue] += 1
        assignedqueues = []
        for i in range(len(customer_info)):
            customer_info_sortfood[i]['queue'] = queue
        return customer_info_sortfood, list_queued_customers

    def service(meancash, meancard, fractioncash, queue, list_queued_customers,customer_info):
        for i in range(len(customer_info)):
            if customer_info[i]['cash']:
                servicetime = random.exponential(meancash) #servicetime cash
            else:
                servicetime = random.exponential(meancard) #servicetime card
            customer_info[i]['servicetime'] = servicetime
        
        
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
customer_info = customer.customer_info([0,6,20,30],[10,60,30,50],0.4)
print(customer_info.items())
sorted_customer_info = sorted(customer_info.items(),key=lambda item: (item[1]['t_foodtaken']))
print(sorted_customer_info)
print(sorted_customer_info[3])
# print(customer.take_food(80, [1,2]))
# print(service.assign_to_queue([3,0,1],customer_info))