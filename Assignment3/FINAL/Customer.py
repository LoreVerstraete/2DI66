class Customer :
    ''' Describes customer actions '''

    MOVETIME = 1

    def __init__(self, arrival, destinationFloor, startFloor, custnr=None):
        ''' 
        Initialise the elevators
        '''
        self.arrivalTime = arrival
        self.destinationFloor = destinationFloor
        self.startFloor = startFloor 
        if self.destinationFloor > self.startFloor: #checks if customer wants up or down 
            self.directionUp = True 
        else: 
            self.directionUp = False
        self.floordiff = abs(startFloor-destinationFloor)
        self.custnr = custnr

    def impatience(self,impatienceDown, impatienceUp): 
        ''' 
        Calculates the time at which a customer leaves the queue 
            due to impatience (if it does not enter the elevator
            before this time)
        Returns:
            time described above
        '''
        if self.directionUp:
            impatienceTime = impatienceUp[self.floordiff]  
        else:
            impatienceTime = impatienceDown[self.floordiff]
        return impatienceTime     
            

    def __str__(self):
        ''' 
        Returns string with information of the customer
        '''
        return "Customer "+ str(self.custnr) + " arrives at floor "+ str(self.startFloor) + " at time " + str(self.arrivalTime) + " with destination floor " + str(self.destinationFloor)