from Elevator import Elevator
from numpy import zeros

class Results:
    ''' Calculates the results.'''

    def __init__(self, numbersOfAllElevators):
        self.sumWaitingTime = zeros(Elevator.FLOORS)
        self.sumPeopleInTheElevator = zeros(numbersOfAllElevators)
        self.totalTime = 0
        self.allPeople = zeros(Elevator.FLOORS)   
        self.oldTime = zeros(numbersOfAllElevators)  
        self.numbersOfAllElevators = numbersOfAllElevators
        self.enterCustomer = zeros(Elevator.FLOORS)
        self.waitedCustomer = zeros(Elevator.FLOORS)
        self.customerLongerThan5 = 0

    def getMeanWaitingTime(self):
        return self.sumWaitingTime / self.allPeople
    
    def registerPeopleInElevator(self, t, peopleInElevator, nrElevator):
        self.sumPeopleInTheElevator[nrElevator] += peopleInElevator*(t-self.oldTime[nrElevator])
        self.oldTime[nrElevator] = t
        
    def getMeanOfPeopleInTheElevator(self):
        print(self.sumPeopleInTheElevator)
        print(self.totalTime)
        return self.sumPeopleInTheElevator / (self.totalTime)

    def getProbabilityNoEntery(self):
        return self.waitedCustomer/(self.enterCustomer + self.waitedCustomer)
    
    def fractionLongerThan5(self):
        print(self.allPeople)
        print(sum(self.allPeople))
        return self.customerLongerThan5 / sum(self.allPeople)

    
    def __str__(self):
        return ("Mean waiting time: " + str(self.getMeanWaitingTime()) + "\n" 
                + "mean of People in the Elevator: " + str(self.getMeanOfPeopleInTheElevator())+ "\n" 
                + "probability to not to enter the elevator because if the limit: " + str(self.getProbabilityNoEntery()) + "\n"
                + "Total number of customers: " +str(self.allPeople) + "\n"
                + "Total run time: " +str(self.totalTime))
    
