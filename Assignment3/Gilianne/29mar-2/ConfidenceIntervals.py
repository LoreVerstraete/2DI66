import time
from numpy import mean, var, sqrt, array, zeros
from Elevator import Elevator 

class ConfidenceIntervals: 

    def __init__(self, WaitingTime, PeopleInTheElevator, noEnteryLimitOfTheElevator, nrRuns):
        self.WaitingTime = WaitingTime
        self.PeopleInTheElevator = PeopleInTheElevator
        self.noEnteryLimitOfTheElevator = noEnteryLimitOfTheElevator
        self.nrRuns = nrRuns

    def getCIWaitingTime(self):
        confidenceIntervals = zeros(Elevator.FLOORS*2).reshape((Elevator.FLOORS,2)) 
        means = [0] * Elevator.FLOORS
        for i in range(Elevator.FLOORS): 
            waitingTimeFloor = array(self.WaitingTime)[:,i]
            confidenceIntervals[i][0] = mean(waitingTimeFloor) - 1.96*sqrt(var(waitingTimeFloor)/self.nrRuns)
            confidenceIntervals[i][1] = mean(waitingTimeFloor) + 1.96*sqrt(var(waitingTimeFloor)/self.nrRuns)
            means[i] = mean(waitingTimeFloor) 
        return confidenceIntervals, means
    
    def getCIPeopleInTheElevator(self):
        lb = mean(self.PeopleInTheElevator) - 1.96*sqrt(var(self.PeopleInTheElevator)/self.nrRuns)
        ub = mean(self.PeopleInTheElevator) + 1.96*sqrt(var(self.PeopleInTheElevator)/self.nrRuns)
        means = mean(self.PeopleInTheElevator)
        return [lb, means, ub]
    
    def getCIProbabilityNoEntery(self):
        confidenceIntervals = zeros(Elevator.FLOORS*2).reshape((Elevator.FLOORS,2))
        means = zeros(Elevator.FLOORS) # [0] * Elevator.FLOORS
        for i in range(Elevator.FLOORS): 
            noEntry = array(self.noEnteryLimitOfTheElevator)[:,i]
            # print("no Entry: ", noEntry, "means", mean(noEntry))
            # print(array(self.noEnteryLimitOfTheElevator))
            confidenceIntervals[i][0] = mean(noEntry) - 1.96*sqrt(var(noEntry)/self.nrRuns)
            confidenceIntervals[i][1] = mean(noEntry) + 1.96*sqrt(var(noEntry)/self.nrRuns)
            means[i] = mean(noEntry)
        return confidenceIntervals, means
    
    
    
    
    
    # def getCIProbabilityNoEntery(self):
    #     confidenceIntervals = zeros(Elevator.FLOORS*2).reshape((Elevator.FLOORS,2))
    #     means = zeros(Elevator.FLOORS) # [0] * Elevator.FLOORS
    #     for i in range(Elevator.FLOORS): 
    #         noEntry = array(self.noEnteryLimitOfTheElevator)[:,i]
    #         print("no Entry: ", noEntry, "means", mean(noEntry))
    #         print(array(self.noEnteryLimitOfTheElevator))
    #         confidenceIntervals[i][0] = mean(noEntry) - 1.96*sqrt(var(noEntry)/self.nrRuns)
    #         confidenceIntervals[i][1] = mean(noEntry) + 1.96*sqrt(var(noEntry)/self.nrRuns)
    #         means[i] = mean(noEntry)
    #     return confidenceIntervals, means

    def __str__(self):
        cIWaitingTime = self.getCIWaitingTime()
        cIProbabilityNoEntry = self.getCIProbabilityNoEntery()
        return ("Confidence Intervalls of the mean waiting time: " + "\n" + 
                "Floor 0: " + "[ " + str(round(cIWaitingTime[0][0][0],4)) + " , " + str(round(cIWaitingTime[1][0],4)) + " , " + str(round(cIWaitingTime[0][0][1],4)) + " ]" + "\n" + 
                "Floor 1: " + "[ " + str(round(cIWaitingTime[0][1][0],4)) + " , " + str(round(cIWaitingTime[1][1],4)) + " , " + str(round(cIWaitingTime[0][1][1],4)) + " ]" + "\n" +
                "Floor 2: " + "[ " + str(round(cIWaitingTime[0][2][0],4)) + " , " + str(round(cIWaitingTime[1][2],4)) + " , " + str(round(cIWaitingTime[0][2][1],4)) + " ]" + "\n" +
                "Floor 3: " + "[ " + str(round(cIWaitingTime[0][3][0],4)) + " , " + str(round(cIWaitingTime[1][3],4)) + " , " + str(round(cIWaitingTime[0][3][1],4)) + " ]" + "\n" +
                "Floor 4: " + "[ " + str(round(cIWaitingTime[0][4][0],4)) + " , " + str(round(cIWaitingTime[1][4],4)) + " , " + str(round(cIWaitingTime[0][4][1],4)) + " ]" + "\n" +
                "Confidence Intervalls of the  number of people in the elevators: " + "[ " + str(round(self.getCIPeopleInTheElevator()[0],4)) + " , " + str(round(self.getCIPeopleInTheElevator()[1],4)) + " ,  " + str(round(self.getCIPeopleInTheElevator()[2],4)) + " ]" + "\n" +
                "Confidence Intervals pf the probability of no entry because of a full elevator: " + "\n" +
                "Floor 0: " + "[ " + str(round(cIProbabilityNoEntry[0][0][0],10)) + " , " + str(round(cIProbabilityNoEntry[1][0],10)) + " , " + str(round(cIProbabilityNoEntry[0][0][1],10)) + " ]" + "\n" +
                "Floor 1: " + "[ " + str(round(cIProbabilityNoEntry[0][1][0],4)) + " , " + str(round(cIProbabilityNoEntry[1][1],4)) + " , " + str(round(cIProbabilityNoEntry[0][1][1],4)) + " ]" + "\n" +
                "Floor 2: " + "[ " + str(round(cIProbabilityNoEntry[0][2][0],4)) + " , " + str(round(cIProbabilityNoEntry[1][2],4)) + " , " + str(round(cIProbabilityNoEntry[0][2][1],4)) + " ]" + "\n" +
                "Floor 3: " + "[ " + str(round(cIProbabilityNoEntry[0][3][0],4)) + " , " + str(round(cIProbabilityNoEntry[1][3],4)) + " , " + str(round(cIProbabilityNoEntry[0][3][1],4)) + " ]" + "\n" +
                "Floor 4: " + "[ " + str(round(cIProbabilityNoEntry[0][4][0],4)) + " , " + str(round(cIProbabilityNoEntry[1][4],4)) + " , " + str(round(cIProbabilityNoEntry[0][4][1],4)) + " ]" + "\n" ) 
    