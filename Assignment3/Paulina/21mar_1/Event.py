import Elevator as Elevator 
import Customer as Customer 

class Event:

    ARRIVAL = 0 
    DEPARTURE = 1
    ELEVATORSTOPS = 2


    def __init__(self, typ, arrivaltime, startfloor, destinationFloor, directionUp ,cust = None):
        self.type = typ
        self.arrtime = arrivaltime 
        self.customer = cust
        self.floor = startfloor 
        self.directionUp = directionUp
        self.destinationFloor = destinationFloor

# arrivalTime, destinationFloor, startFloor, directionUp
    def __lt__(self, other):
        '''
        sorting the event list. 
        '''
        return self.arrtime < other.arrtime
    
    def __str__(self):
        st = ("arrival", "departure", "elevator stops")
        return st[self.type] + " of customer " + str(self.customer) + " at time t: " +str(self.arrtime) +" start Floor: "+ str(self.floor) + " the deniation floor " + str(self.destinationFloor)

    


    



#test: 
#e = Event(2,1,1)
#print(e)