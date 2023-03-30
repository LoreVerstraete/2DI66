import Elevator as Elevator 
import Customer as Customer 

class Event:

    ARRIVAL = 0 
    ELEVATORSTOPS = 1
    IMPATIENT = 2


    def __init__(self, typ, time, floor = None, elevator = None, customer = None):
        self.type = typ
        self.time = time 
        self.elevatorNr = elevator
        self.floor = floor 
        self.customer = customer

    def __lt__(self, other):
        '''
        sorting the event list. 
        '''
        return self.time < other.time
    
    def __str__(self):
        st = ("arrival", "elevator stops", "impatient customer takes stairs")
        if st[self.type] == "elevator stops":
            return st[self.type] + "nr elevator "+ str(self.elevatorNr) + " at time " + str(self.time)
        elif st[self.type] == "arrival":
            return st[self.type] + " of customer at time " +str(self.time) + " at floor " + str(self.floor)
        else:
            return "impatient customer at floor "+ str(self.floor)+" leaves the queue at time"+ str(self.time)

    # def doors(self, time, floor):
    #     self.time = time
    #     Elevator.floor = floor # add number of Elevator 



    



#test: 
#e = Event(2,1,1)
#print(e)