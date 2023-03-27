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

    def movingDoors(self, doorDist):  #time of the door openong/closing 
        self.doorDist = doorDist

    def checkIfStop(self, destinationFloors):
        "checks if there is a customer that want to get out of the elevator at this floor"
        if  self.floornumber in destinationFloors:
            return True 
        else:
            return False 
        
    def newFloor(self, floornumber):
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
    