from Customer import Customer

class Elevator:
    ''' Describes the elevator processes '''
    
    moveTime = 6
    maxPeople = 10
    floors = 4

    def __init__(self,elevatorNumber):
        self.elevatorNumber = elevatorNumber
        self.numberOfPeople = 0 # at the start there are no people in the elevators 
        self.floor = 0 # all th elevators start start at the ground floor 
        self.directionUp = True # if moving down than false 


    def movingDoors(self, doorDist):  #time of the door openong/closing 
        self.doorDist = doorDist

    def checkIfStop(self, destinationFloors, floor):
        "checks if there is a customer that want to get out of the elevator at this floor"
        if floor in destinationFloors:
            return True 
        else:
            return False 
        
    def newFloor(self, floornumber, directionUp):
        """
        Calculates the new floor.
        """
        if directionUp:
            return floornumber + 1
        else:
            return floornumber - 1

        

'''
    def stopElevator(self, floor, customer):
        self.floor = floor 
        Elevator.movingDoors()
        Elevator.enterElevator()
        Customer.leaveElevator()
        Elevator.movingDoors()
'''

    
    #def moveElevator(self,nrFloors):


    

    