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

    def __init__(self, arrival, destinationFloor, startFloor):
        ''' Customer has the Atributes: arrivalTime, destinationFloor, startFloor, directionUp '''
        self.arrivalTime = arrival
        self.destinationFloor = destinationFloor
        self.startFloor = startFloor 
        if self.destinationFloor > self.startFloor: #checks if it moves up or down 
            self.directionUp = True 
        else: 
            self.directionUp = False

    def __str__(self):
        return "Customer at " + str(self.arrivalTime)

    # def moveTo(self, floor, position): 
    #     """
    #     move to and from the elevator.
    #     """ 
    #     self.position = position # 0 if still in the queue 
    #     self.floor  = floor # at what floor they are 

    # def directionCustomer(self, currentFloor, destinationFloor):
    #     if max(currentFloor, destinationFloor) == currentFloor: 
    #         return False # move up 
    #     else: 
    #         return True # move down 

# c = Customer(10, 3, 1)
# print(c)