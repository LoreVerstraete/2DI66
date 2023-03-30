import time
from numpy import mean, var, sqrt, array, zeros, std
from Elevator import Elevator 
from Results import Results

class ConfidenceIntervals: 

    def __init__(self, WaitingTime, PeopleInTheElevator, noEnteryLimitOfTheElevator, nrRuns, nrElevators):
        self.WaitingTime = WaitingTime
        self.PeopleInTheElevator = PeopleInTheElevator
        self.noEnteryLimitOfTheElevator = noEnteryLimitOfTheElevator
        self.nrRuns = nrRuns
        self.nrElevators = nrElevators
        

    def getCIWaitingTime(self):
        confidenceIntervals = zeros(Elevator.FLOORS*2).reshape((Elevator.FLOORS,2)) 
        means = [0] * Elevator.FLOORS
        standardDerivation = [0] * Elevator.FLOORS
        for i in range(Elevator.FLOORS): 
            waitingTimeFloor = array(self.WaitingTime)[:,i]
            confidenceIntervals[i][0] = mean(waitingTimeFloor) - 1.96*sqrt(var(waitingTimeFloor)/self.nrRuns)
            confidenceIntervals[i][1] = mean(waitingTimeFloor) + 1.96*sqrt(var(waitingTimeFloor)/self.nrRuns)
            means[i] = mean(waitingTimeFloor) 
            standardDerivation[i] = std(waitingTimeFloor)
        return confidenceIntervals, means, standardDerivation
    
    def getCIPeopleInTheElevator(self):
        
        confidenceIntervals = zeros(self.nrElevators*2).reshape((self.nrElevators,2)) 
        means = [0] * self.nrElevators
        standardDerivation = [0] * self.nrElevators
        for i in range(self.nrElevators): 
            nrPeopleInElevator = array(self.PeopleInTheElevator)[:,i]
            confidenceIntervals[i][0] = mean(nrPeopleInElevator) - 1.96*sqrt(var(nrPeopleInElevator)/self.nrRuns)
            confidenceIntervals[i][1] = mean(nrPeopleInElevator) + 1.96*sqrt(var(nrPeopleInElevator)/self.nrRuns)
            means[i] = mean(nrPeopleInElevator) 
            standardDerivation[i] = std(nrPeopleInElevator)
        return confidenceIntervals, means, standardDerivation
        
        # lb = mean(self.PeopleInTheElevator) - 1.96*sqrt(var(self.PeopleInTheElevator)/self.nrRuns)
        # ub = mean(self.PeopleInTheElevator) + 1.96*sqrt(var(self.PeopleInTheElevator)/self.nrRuns)
        # means = mean(self.PeopleInTheElevator)
        # return [lb, means, ub]
    
    def getCIProbabilityNoEntery(self):
        confidenceIntervals = zeros(Elevator.FLOORS*2).reshape((Elevator.FLOORS,2))
        means = zeros(Elevator.FLOORS) 
        standardDerivation = zeros(Elevator.FLOORS) 
        for i in range(Elevator.FLOORS): 
            noEntry = array(self.noEnteryLimitOfTheElevator)[:,i]
            # print("no Entry: ", noEntry, "means", mean(noEntry))
            # print(array(self.noEnteryLimitOfTheElevator))
            confidenceIntervals[i][0] = mean(noEntry) - 1.96*sqrt(var(noEntry)/self.nrRuns)
            confidenceIntervals[i][1] = mean(noEntry) + 1.96*sqrt(var(noEntry)/self.nrRuns)
            means[i] = mean(noEntry)
            standardDerivation[i] = std(noEntry)
        return confidenceIntervals, means, standardDerivation

    def __str__(self):
        cIWaitingTime = self.getCIWaitingTime()
        cIProbabilityNoEntry = self.getCIProbabilityNoEntery()
        cIProbabilityPeopleInElevator = self.getCIPeopleInTheElevator()
        strElevator = ""
        for i in range(self.nrElevators):
            strElevator += (("Elevator "+ str(i) + " [ " + str(round(cIProbabilityPeopleInElevator[0][i][0],4)) + " , " + str(round(cIProbabilityPeopleInElevator[1][i],4))+ " , " + str(round(cIProbabilityPeopleInElevator[0][i][1],4)) + " ] Standard Deriviation: " + str(round(cIProbabilityPeopleInElevator[2][i],4)) + "\n"))
        strWaitingTime = ""
        strProbabilityNoEntry = ""
        for i in range(Elevator.FLOORS):
            strWaitingTime += ("Floor " + str(i) + ": " +str(round(cIWaitingTime[0][i][0],4)) + " , " + str(round(cIWaitingTime[1][i],4)) + " , " + str(round(cIWaitingTime[0][0][1],4)) + " ] Standard Derivation: " + str(round(cIWaitingTime[2][i],4)) + "\n")
            strProbabilityNoEntry += ("Floor "+ str(i) +": " + "[ " + str(round(cIProbabilityNoEntry[0][0][0],10)) + " , " + str(round(cIProbabilityNoEntry[1][0],10)) + " , " + str(round(cIProbabilityNoEntry[0][0][1],10)) + " ] Standard Derivation: " + str(round(cIProbabilityNoEntry[2][i],4)) + "\n")
        return ("Confidence Intervalls of the mean waiting time: " + "\n" + 
                strWaitingTime +
                "Confidence Intervalls of the  number of people in the elevators: " + "\n" +
                strElevator +
                "Confidence Intervals pf the probability of no entry because of a full elevator: " + "\n" +
                strProbabilityNoEntry) 
    



"""
                "Floor 0: " + "[ " + str(round(cIProbabilityNoEntry[0][0][0],10)) + " , " + str(round(cIProbabilityNoEntry[1][0],10)) + " , " + str(round(cIProbabilityNoEntry[0][0][1],10)) + " ]" + "\n" +
                "Floor 1: " + "[ " + str(round(cIProbabilityNoEntry[0][1][0],4)) + " , " + str(round(cIProbabilityNoEntry[1][1],4)) + " , " + str(round(cIProbabilityNoEntry[0][1][1],4)) + " ]" + "\n" +
                "Floor 2: " + "[ " + str(round(cIProbabilityNoEntry[0][2][0],4)) + " , " + str(round(cIProbabilityNoEntry[1][2],4)) + " , " + str(round(cIProbabilityNoEntry[0][2][1],4)) + " ]" + "\n" +
                "Floor 3: " + "[ " + str(round(cIProbabilityNoEntry[0][3][0],4)) + " , " + str(round(cIProbabilityNoEntry[1][3],4)) + " , " + str(round(cIProbabilityNoEntry[0][3][1],4)) + " ]" + "\n" +
                "Floor 4: " + "[ " + str(round(cIProbabilityNoEntry[0][4][0],4)) + " , " + str(round(cIProbabilityNoEntry[1][4],4)) + " , " + str(round(cIProbabilityNoEntry[0][4][1],4)) + " ]" + "\n" 

"Floor 0: " + "[ " + str(round(cIWaitingTime[0][0][0],4)) + " , " + str(round(cIWaitingTime[1][0],4)) + " , " + str(round(cIWaitingTime[0][0][1],4)) + " ]" + "\n" + 
"Floor 1: " + "[ " + str(round(cIWaitingTime[0][1][0],4)) + " , " + str(round(cIWaitingTime[1][1],4)) + " , " + str(round(cIWaitingTime[0][1][1],4)) + " ]" + "\n" +
"Floor 2: " + "[ " + str(round(cIWaitingTime[0][2][0],4)) + " , " + str(round(cIWaitingTime[1][2],4)) + " , " + str(round(cIWaitingTime[0][2][1],4)) + " ]" + "\n" +
"Floor 3: " + "[ " + str(round(cIWaitingTime[0][3][0],4)) + " , " + str(round(cIWaitingTime[1][3],4)) + " , " + str(round(cIWaitingTime[0][3][1],4)) + " ]" + "\n" +
"Floor 4: " + "[ " + str(round(cIWaitingTime[0][4][0],4)) + " , " + str(round(cIWaitingTime[1][4],4)) + " , " + str(round(cIWaitingTime[0][4][1],4)) + " ]" + "\n" + """