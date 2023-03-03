from customer import customer

class service:
    # This class determines the service times, which are exponentially distributed
    # with means 20 and 12 seconds for payment by cash and card, respectively. It has
    # been observed that 40 % of customers pay cash.
    # 3 cashiers
        
    def assign_to_queue(total_nr_queues, queue_time_customer, list_queued_customers_old)
        # assign customer to the shortest queue
        # list_queued_customers_old = [2 3 4]
        # list_queued_customers_old[queue] += 1
        # list_queued_customers_new = list_queued_customers_old
        # output queue, list_queued_customers_new

    def service(meancash, meancard, cashpercentage, list_queued_customers_old)
        # first calc if it is card or cash (random 40% cash)
        # service times are exponentially distributed with means 20 for cash
        # service times are exponentially distributed with means 12 for card
        # timefinished = save time customer leaves the cashier
        # timequeued = timefinished - servicetime - que
        # list_queued_customers_old[queue] -= 1
        # list_queued_customers_new = list_queued_customers_old
        # output servicetime, list_queued_customers_new
            
        