from Customer import Customer

class Elevator:
    ''' Describes the elevator processes '''
    
    moveTime = 6
    maxPeople = 10
    floors = 5

    def __init__(self,elevatorNumber):
        self.elevatorNumber = elevatorNumber
        self.numberOfPeople = 0 # at the start there are no people in the elevators 
        self.floor = 0 # all th elevators start start at the ground floor 
        self.directionUp = True # if moving down than false 

    def movingDoors(self, doorDist):
        self.doorDist = doorDist

    def stopElevator(self, customer):
        Elevator.movingDoors()
        Elevator.enterElevator()
        Customer.leaveElevator()
        Elevator.movingDoors()

    #def moveElevator(self,nrFloors):


    

    