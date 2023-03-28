from Customer import Customer

class Elevator:
    ''' Describes the elevator processes '''
    
    MOVETIME = 6
    MAXPEOPLE = 10
    FLOORS = 5

    def __init__(self,timeArrAtFloor, elevatorNumber, floornumber=None):
        self.timeArrAtFloor = timeArrAtFloor ####added arrival time
        self.elevatorNumber = elevatorNumber
        self.floornumber = floornumber #0 # all the elevators start start at the ground floor 
        self.directionUp = True # if moving down than false 
        self.destinationFloor = []
        self.stopElevator = False
        
    def newFloor(self):
        """
        Calculates the new floor.
        """
        if self.directionUp:
            self.floornumber += 1
            if self.floornumber == Elevator.FLOORS-1:
                self.directionUp = False
        else:
            self.floornumber -= 1   
            if self.floornumber == 0:
                self.directionUp = True
    
    def checkLeaving(self, queueElevator_elevator):
        removeCustomers = []
        for customer_elevator in queueElevator_elevator: 
                    if customer_elevator.destinationFloor == self.floornumber: 
                        removeCustomers.append(customer_elevator)
        return removeCustomers
    
    def checkEntering(self, queueFloor_elevator):
        addCustomers = []
        for customer_floor in queueFloor_elevator:
            if customer_floor.directionUp == self.directionUp:
                addCustomers.append(customer_floor)
        return addCustomers 