"""
-	Users:
    	Attributes:
        	Arrival time 
        	waiting time    
            Time in the elevators 
        	(leaving time)
    	Events: 
        	Arrival 
        	Waiting     
            Elevator 
        	Leaving 
"""

class Customer :
    enteringTime = 1
    leavingTime = 1

    def __init__(self, arrival, destinationFloor, startFloor):
        self.arrivalTime = arrival
        self.enterTime = 0 #arriving time + waitingtime, timestamp it starts to enter
        self.leaveTime = 0 #arriving time + waitingtime + servicetime, timestamp it ends leaving
        self.destinationFloor = destinationFloor
        self.startFloor = startFloor 

        #self.waitingTime = 0 


    def moveTo(self, floor, position ): 
        """
        move to and from the elevator.
        """ 
        self.position = position 
        self.floor  = floor 

    
    #def enterElevator(self):
        
   
    #def leaveElevator(self):

    
    def __str__(self):
        return "Customer at " + str(self.arrivalTime)

c = Customer(10)
print(c)