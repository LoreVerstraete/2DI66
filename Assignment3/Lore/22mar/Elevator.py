from Customer import Customer

class Elevator:
    ''' Describes the elevator processes '''
    
    MOVETIME = 6
    MAXPEOPLE = 10
    FLOORS = 4

    def __init__(self,elevatorNumber):
        self.elevatorNumber = elevatorNumber
        self.numberOfPeople = 0 # at the start there are no people in the elevators 
        self.floor = 0 # all th elevators start start at the ground floor 
        self.directionUp = True # if moving down than false 
        self.destinationFloor = []
        self.stopElevator = False


    def movingDoors(self, doorDist, t):  #time of the door openong/closing 
        t += doorDist
        return t

    def checkIfStop(self, destinationFloors):
        "checks if there is a customer that want to get out of the elevator at this floor"
        if self.floor in destinationFloors:
            return True 
        else:
            return False 
        
    def newFloor(self, t):
        """
        Calculates the new floor.
        """
        if self.directionUp:
            self.floor += 1
            if self.floor == 4:
                self.directionUp = False
        else:
            self.floor -= 1
            if self.floor == 0:
                self.directionUp = True
        t += Elevator.MOVETIME
        return t

    
    # def checkStop(self, floor, destinationFloor):
    #     self.stopElevator= destinationFloor.count(floor)

'''
    def stopElevator(self, floor, customer):
        self.floor = floor 
        Elevator.movingDoors()
        Elevator.enterElevator()
        Customer.leaveElevator()
        Elevator.movingDoors()
'''

    
    #def moveElevator(self,nrFloors):


    

    