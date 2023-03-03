from service import service
from customer import customer
from numpy import zeros

class Simulation:
    # simulate use cases
    # for 1 hour: 12.00h-13.00h

    poissonratearrivals = 0.1
    meangroupsize = 3
    meanfood = 80 #seconds
    total_nr_queues = 3
    list_queued_customers_old = zeros(total_nr_queues)

    def sim(meangroupsize, poissonratearrivals, meanfood,total_nr_queues,list_queued_customers_old)
        # listofarrivals, groupnumber, individualnumber = arrive(meangroupsize, poissonratearrivals)
        # time_customer_arrives_at_queue, list_time_it_takes_to_get_food_per_individual = take_food(meanfood)
        # queue, list_queued_customers_new = assign_to_queue(total_nr_queues, time_customer_arrives_at_queue, list_queued_customers_old)
        # if queue > 1:
        #       servicetime = service(meancash, meancard, cashpercentage)
        # 
