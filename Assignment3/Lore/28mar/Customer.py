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

    MOVETIME = 1

    def __init__(self, arrival, destinationFloor, startFloor, custnr=None):
        ''' Customer has the Atributes: arrivalTime, destinationFloor, startFloor, directionUp '''
        self.arrivalTime = arrival
        self.destinationFloor = destinationFloor
        self.startFloor = startFloor 
        if self.destinationFloor > self.startFloor: #checks if it moves up or down 
            self.directionUp = True 
        else: 
            self.directionUp = False
        self.floordiff = abs(startFloor-destinationFloor)
        self.custnr = custnr

    def impatience(self,impatienceDown, impatienceUp): 
        if self.directionUp:
            impatienceTime = impatienceUp[self.floordiff]  
        else:
            impatienceTime = impatienceDown[self.floordiff]
        return impatienceTime     
            

    def __str__(self):
        return "Customer "+ str(self.custnr) + " arrives at floor "+ str(self.startFloor) + " at time " + str(self.arrivalTime) + " with destination floor " + str(self.destinationFloor)
