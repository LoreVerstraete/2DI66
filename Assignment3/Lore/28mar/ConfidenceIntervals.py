import time
from numpy import mean, var, sqrt, array, shape 
from Elevator import Elevator 

class ConfidenceIntervals: 

    def __init__(self, WaitingTime, PeopleInTheElevator, noEnteryLimitOfTheElevator, nrRuns):
        self.WaitingTime = WaitingTime
        self.PeopleInTheElevator = PeopleInTheElevator
        self.noEnteryLimitOfTheElevator = noEnteryLimitOfTheElevator
        self.nrRuns = nrRuns

    def getCIWaitingTime(self):
        confidenceIntervals = [[0,0]] * Elevator.FLOORS
        means = [0] * Elevator.FLOORS
        for i in range(Elevator.FLOORS): 
            waitingTimeFloor = array(self.WaitingTime)[:,i]
            confidenceIntervals[i][0] = mean(waitingTimeFloor) - 1.96*sqrt(var(waitingTimeFloor)/self.nrRuns)
            confidenceIntervals[i][1] = mean(waitingTimeFloor) + 1.96*sqrt(var(waitingTimeFloor)/self.nrRuns)
            means[i] = mean(waitingTimeFloor) 
        return confidenceIntervals, means
    
    def getCIPeopleInTheElevator(self):
        lb = mean(self.PeopleInTheElevator) - 1.96*sqrt(var(self.PeopleInTheElevator)/self.nrRuns)
        ub = mean(self.PeopleInTheElevator) +- 1.96*sqrt(var(self.PeopleInTheElevator)/self.nrRuns)
        means = mean(self.PeopleInTheElevator)
        return [lb, means, ub]
    
    def getCIProbabilityNoEntery(self):
        confidenceIntervals = [[0,0]]* Elevator.FLOORS
        means = [0] * Elevator.FLOORS
        for i in range(Elevator.FLOORS): 
            noEntry = array(self.noEnteryLimitOfTheElevator)[:,i]
            confidenceIntervals[i][0] = mean(noEntry) - 1.96*sqrt(var(noEntry)/self.nrRuns)
            confidenceIntervals[i][1] = mean(noEntry) + 1.96*sqrt(var(noEntry)/self.nrRuns)
            means[i] = mean(noEntry)
        return confidenceIntervals, means

    def __str__(self):
        print(str(self.getCIPeopleInTheElevator()))
        print(str(self.getCIWaitingTime()[0][0][0]))
        print(str(self.getCIWaitingTime()[1][0]))
        return ("Confidence Intervalls of the mean waiting time: " + "\n" + 
                "Floor 1: " + "[ " + str(round(self.getCIWaitingTime()[0][0][0],4)) + " , " + str(round(self.getCIWaitingTime()[1][0],4)) + " , " + str(round(self.getCIWaitingTime()[0][0][1],4)) + " ]"  + "\n" + 
                "Floor 2: " + "[ " + str(round(self.getCIWaitingTime()[0][1][0],4)) + " , " + str(round(self.getCIWaitingTime()[1][1],4)) + " , " + str(round(self.getCIWaitingTime()[0][1][1],4)) + " ]" + "\n" +
                "Floor 3: " + "[ " + str(round(self.getCIWaitingTime()[0][2][0],4)) + " , " + str(round(self.getCIWaitingTime()[1][2],4)) + " , " + str(round(self.getCIWaitingTime()[0][2][1],4)) + " ]" + "\n" +
                "Floor 4: " + "[ " + str(round(self.getCIWaitingTime()[0][3][0],4)) + " , " + str(round(self.getCIWaitingTime()[1][3],4)) + " , " + str(round(self.getCIWaitingTime()[0][3][1],4)) + " ]" + "\n" +
                "Floor 5: " + "[ " + str(round(self.getCIWaitingTime()[0][4][0],4)) + " , " + str(round(self.getCIWaitingTime()[1][4],4)) + " , " + str(round(self.getCIWaitingTime()[0][4][1],4)) + " ]" + "\n" +
                "Confidence Intervalls of the  number of people in the elevators: " + "[ " + str(round(self.getCIPeopleInTheElevator()[0],4)) + " , " + str(round(self.getCIPeopleInTheElevator()[1],4)) + " ,  " + str(round(self.getCIPeopleInTheElevator()[2],4)) + " ]" + "\n" +
                "Confidence Intervals pf the probability of no entry because of a full elevator: " + "\n" +
                "Floor 1: " + "[ " + str(round(self.getCIProbabilityNoEntery()[0][0][0],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[1][0],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[0][0][1],4)) + " ]" + "\n" +
                "Floor 2: " + "[ " + str(round(self.getCIProbabilityNoEntery()[0][1][0],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[1][1],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[0][1][1],4)) + " ]" + "\n" +
                "Floor 3: " + "[ " + str(round(self.getCIProbabilityNoEntery()[0][2][0],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[1][2],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[0][2][1],4)) + " ]" + "\n" +
                "Floor 4: " + "[ " + str(round(self.getCIProbabilityNoEntery()[0][3][0],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[1][3],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[0][3][1],4)) + " ]" + "\n" +
                "Floor 5: " + "[ " + str(round(self.getCIProbabilityNoEntery()[0][4][0],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[1][4],4)) + " , " + str(round(self.getCIProbabilityNoEntery()[0][4][1],4)) + " ]" + "\n" ) 
    