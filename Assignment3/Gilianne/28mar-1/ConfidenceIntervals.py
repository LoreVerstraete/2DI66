import time
from numpy import mean, var, sqrt, array
from Elevator import Elevator 

class ConfidenceIntervals: 

    def __init__(self, WaitingTime, PeopleInTheElevator, noEnteryLimitOfTheElevator, nrRuns):
        self.WaitingTime = WaitingTime
        self.PeopleInTheElevator = PeopleInTheElevator
        self.noEnteryLimitOfTheElevator = noEnteryLimitOfTheElevator
        self.nrRuns = nrRuns

    def getCIWaitingTime(self):
        confidenceIntervals = [[0,0]]* Elevator.FLOORS
        for i in range(Elevator.FLOORS): 
            waitingTimeFloor = array(self.WaitingTime)[:,i]
            confidenceIntervals[i][0] = mean(waitingTimeFloor) - 1.96*sqrt(var(waitingTimeFloor)/self.nrRuns)
            confidenceIntervals[i][1] = mean(waitingTimeFloor) + 1.96*sqrt(var(waitingTimeFloor)/self.nrRuns)
        return confidenceIntervals
    
    def getCIPeopleInTheElevator(self):
        lb = mean(self.PeopleInTheElevator) - 1.96*sqrt(var(self.PeopleInTheElevator)/self.nrRuns)
        ub = mean(self.PeopleInTheElevator) +- 1.96*sqrt(var(self.PeopleInTheElevator)/self.nrRuns)
        return [lb, ub]
    
    def getCIProbabilityNoEntery(self):
        confidenceIntervals = [[0,0]]* Elevator.FLOORS
        for i in range(Elevator.FLOORS): 
            noEntry = array(self.noEnteryLimitOfTheElevator)[:,i]
            confidenceIntervals[i][0] = mean(noEntry) - 1.96*sqrt(var(noEntry)/self.nrRuns)
            confidenceIntervals[i][1] = mean(noEntry) + 1.96*sqrt(var(noEntry)/self.nrRuns)
        return confidenceIntervals

    def __str__(self):
        return ("Confidence Intervalls of the mean waiting time: " + "\n" + 
                "Floor 1: " + str(self.getCIWaitingTime()[0]) + "\n" +
                "Floor 2: " + str(self.getCIWaitingTime()[1]) + "\n" +
                "Floor 3: " + str(self.getCIWaitingTime()[2]) + "\n" +
                "Floor 4: " + str(self.getCIWaitingTime()[3]) + "\n" +
                "Floor 5: "+ str(self.getCIWaitingTime()[4]) + "\n" +
                "Confidence Intervalls of the  number of people in the elevators: " + str(self.getCIPeopleInTheElevator())+ "\n" +
                "Confidence Intervals pf the probability of no entry because of a full elevator: " + "\n" +
                "Floor 1: " + str(self.getCIProbabilityNoEntery()[0]) + "\n" +
                "Floor 2: " + str(self.getCIProbabilityNoEntery()[1]) + "\n" +
                "Floor 3: " + str(self.getCIProbabilityNoEntery()[2]) + "\n" +
                "Floor 4: " + str(self.getCIProbabilityNoEntery()[3]) + "\n" +
                "Floor 5: " + str(self.getCIProbabilityNoEntery()[4]) + "\n")