import Elevator as Elevator 
import Customer as Customer 

class Event:

    CUSTOMER_ARRIVAL = 11   # customer entering queue
    CUSTOMER_IMPATIENT = 12 # customer leaving queue
    CUSTOMER_ENTER = 13     # customer entering elevator + leaving queue
    CUSTOMER_LEAVE = 14     # customer leaving elevator

    ELEVATOR_STOPS = 21     # elevator stops at floor
    ELEVATOR_OPEN_DOORS = 22 # elevator doors open
    ELEVATOR_CLOSE_DOORS = 23 # elevator doors close


    def __init__(self, typ, time, floor = None, elevatorNr = None, customer = None):
        self.type = typ
        self.time = time 
        self.elevatorNr = elevatorNr
        self.floor = floor 
        self.customer = customer

    def __lt__(self, other):
        '''
        sorting the event list. 
        '''
        return self.time < other.time
    
    def __str__(self):
        if self.type == Event.CUSTOMER_ARRIVAL:
            return "Customer arrival at floor " + str(self.floor) + " at time " + str(self.time) + " and wants to go to floor " + str(self.destfloor)
        elif self.type == Event.CUSTOMER_IMPATIENT:
            return "Impatient customer "+str(self.customer.custnr)+" leaves the queue at time " + str(self.time)
        elif self.type == Event.CUSTOMER_LEAVE:
            return "Customer leaves elevator " + str(self.elevatorNr) + " at time " + str(self.time)
        elif self.type == Event.CUSTOMER_ENTER:
            return "Customer "+ str(self.customer.custnr)+" enters elevator " + str(self.elevatorNr) + " at time " + str(self.time) 
        elif self.type == Event.ELEVATOR_STOPS:
            return "Elevator " + str(self.elevatorNr) + " stops at floor " + str(self.floor) + " at time " + str(self.time)
        elif self.type == Event.ELEVATOR_OPEN_DOORS:
            return "Elevator " + str(self.elevatorNr) + " opens doors at time " + str(self.time)
        elif self.type == Event.ELEVATOR_CLOSE_DOORS:
            return "Elevator " + str(self.elevatorNr) + " closes doors at time " + str(self.time)
        