from Elevator import Elevator
from numpy import zeros

class Results:
    ''' Calculates the results.'''

    def __init__(self, numbersOfAllElevators):
        self.sumWaitingTime = zeros(Elevator.FLOORS)
        self.sumPeopleInTheElevator = 0 
        self.totalTime = 0
        self.noEnteryLimitOfTheElevator = zeros(Elevator.FLOORS)
        self.allPeople = [0] * Elevator.FLOORS
        self.oldTime = [0] * numbersOfAllElevators
        self.numbersOfAllElevators = numbersOfAllElevators
        

    def getMeanWaitingTime(self):
        return self.sumWaitingTime / self.allPeople
    
    def registerPeopleInElevator(self, t, peopleInElevator, nrElevator):
        self.sumPeopleInTheElevator += peopleInElevator*(t-self.oldTime[nrElevator])
        self.oldTime[nrElevator] = t
        
    def getMeanOfPeopleInTheElevator(self):
        return self.sumPeopleInTheElevator / (self.totalTime * self.numbersOfAllElevators) 

    def getProbabilityNoEntery(self):
        return self.noEnteryLimitOfTheElevator / self.allPeople
    
    def __str__(self):
        #st = ("Waiting time ", "people in the elevator ", "probability that a person cann't get into the elevator ")
        return ("Mean waiting time: " + str(self.getMeanWaitingTime()) + "\n" 
                + "mean of People in the Elevator: " + str(self.getMeanOfPeopleInTheElevator())+ "\n" 
                + "probability to not to enter the elevator because if the limit: " + str(self.getProbabilityNoEntery()) + "\n"
                + "Total number of customers: " +str(self.allPeople) + "\n"
                + "Total run time: " +str(self.totalTime))
    

#print(Results())