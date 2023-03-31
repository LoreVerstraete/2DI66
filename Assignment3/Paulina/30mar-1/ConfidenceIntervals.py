from numpy import mean, var, sqrt, array, zeros, std
from Elevator import Elevator 
#from Results import Results

class ConfidenceIntervals: 

    def __init__(self, WaitingTime, PeopleInTheElevator, noEnteryLimitOfTheElevator, nrRuns, nrElevators, fraction5):
        self.WaitingTime = WaitingTime
        self.PeopleInTheElevator = PeopleInTheElevator
        self.noEnteryLimitOfTheElevator = noEnteryLimitOfTheElevator
        self.nrRuns = nrRuns
        self.nrElevators = nrElevators
        self.fraction5 = fraction5
        

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
    
    def getCIProbabilityNoEntery(self):
        confidenceIntervals = zeros(Elevator.FLOORS*2).reshape((Elevator.FLOORS,2))
        means = zeros(Elevator.FLOORS) 
        standardDerivation = zeros(Elevator.FLOORS) 
        for i in range(Elevator.FLOORS): 
            noEntry = array(self.noEnteryLimitOfTheElevator)[:,i]
            confidenceIntervals[i][0] = mean(noEntry) - 1.96*sqrt(var(noEntry)/self.nrRuns)
            confidenceIntervals[i][1] = mean(noEntry) + 1.96*sqrt(var(noEntry)/self.nrRuns)
            means[i] = mean(noEntry)
            standardDerivation[i] = std(noEntry)
        return confidenceIntervals, means, standardDerivation

    def getCIFractionLongerThan5(self):
        confidenceIntervals =[0,0]
        confidenceIntervals[0] = mean(self.fraction5) - 1.96*sqrt(var(self.fraction5)/self.nrRuns)
        confidenceIntervals[1] = mean(self.fraction5) + 1.96*sqrt(var(self.fraction5)/self.nrRuns)
        means = mean(self.fraction5)
        standardDerivative = std(self.fraction5)
        return confidenceIntervals, means, standardDerivative 
    

    def __str__(self):
        cIWaitingTime = self.getCIWaitingTime()
        cIProbabilityNoEntry = self.getCIProbabilityNoEntery()
        cIProbabilityPeopleInElevator = self.getCIPeopleInTheElevator()
        cIfraction5 = self.getCIFractionLongerThan5()
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
                strProbabilityNoEntry + "\n" +
                "fraction of peolpe that are waiting longer than 5 minutes: " + "\n" +
                " [ " + str(round(cIfraction5[0][0],4)) + ", " + str(round(cIfraction5[1],4)) + ", " + str(round(cIfraction5[0][1],4)) + " ] Standard Derivation: " + str(round(cIfraction5[2],4)) ) 
    