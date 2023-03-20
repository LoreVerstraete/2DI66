class Event:

    ARRIVAL = 0 
    DEPARTURE = 1
    ELEVATORSTOPS = 2


    def __init__(self, typ, time, floor, cust = None):
        self.type = typ
        self.time = time 
        self.customer = cust
        self.floor = floor 

    def __lt__(self, other):
        return self.time < other.time
    
    def __str__(self):
        st = ("arrival", "departure", "elevator stops")
        return st[self.type]+ " of customer" + str(self.customer) + " at time t: " +str(self.time)


#test: 
e = Event(1,2)
print(e)