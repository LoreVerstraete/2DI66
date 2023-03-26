import Elevator as Elevator 
import Customer as Customer 

class Event:

    ARRIVAL = 0 
    DEPARTURE = 1
    ELEVATORSTOPS = 2


    def __init__(self, typ, time, floor = None, cust = None):
        self.type = typ
        self.time = time 
        self.customer = cust
        self.floor = floor 

    def __lt__(self, other):
        '''
        sorting the event list. 
        '''
        return self.time < other.time
    
    def __str__(self):
        st = ("arrival", "departure", "elevator stops")
        if st[self.type] == "elevator stops":
            return st[self.type] + " at time " + str(self.time)
        else: 
            return st[self.type] + " of customer at time " +str(self.time) + " at floor " + str(self.floor)

    def doors(self, time, floor):
        self.time = time
        Elevator.floor = floor # add number of Elevator 



    



#test: 
#e = Event(2,1,1)
#print(e)