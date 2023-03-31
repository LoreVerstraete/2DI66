from Customer import Customer
from numpy import zeros 

class Elevator:
    ''' Describes elevator actions '''
    
    MOVETIME = 6
    MAXPEOPLE = 10
    FLOORS = 5

    def __init__(self,timeArrAtFloor, elevatorNumber, numbersOfAllElevators , floornumber=None):
        ''' 
        Initialise the elevators
        '''
        self.timeArrAtFloor = timeArrAtFloor
        self.elevatorNumber = elevatorNumber
        self.floornumber = floornumber 
        self.directionUp = True # if moving down than false 
        self.destinationFloor = [] # next floor of the elevator
        self.stopElevator = False # elevator stops at floor if True, otherwise it goes to next floor
        self.numbersOfAllElevators = numbersOfAllElevators
        
    def newFloor(self):
        '''
        Calculates new floor and the accompanied direction of the elevator
        '''
        if self.directionUp:
            self.floornumber += 1
            if self.floornumber == Elevator.FLOORS-1:
                self.directionUp = False
        else:
            self.floornumber -= 1   
            if self.floornumber == 0:
                self.directionUp = True
    
    def checkLeaving(self, queueElevator_elevator):
        '''
        Check if people want to leave the elevator at a certain floor
        Returns:
            list with all customers that want to leave the elevator
        '''
        removeCustomers = []
        for customer_elevator in queueElevator_elevator: 
                    if customer_elevator.destinationFloor == self.floornumber: 
                        removeCustomers.append(customer_elevator)
        return removeCustomers
    
    def checkEntering(self, queueFloor_elevator):
        '''
        Check if people want to enter the elevator at a certain floor
        Customers only want to enter if the elevator goes in the same direction as they want to go
        Returns:
            list with all customers that want to enter the elevator
        '''
        addCustomers = []
        for customer_floor in queueFloor_elevator:
            if customer_floor.directionUp == self.directionUp:
                addCustomers.append(customer_floor)
        return addCustomers 