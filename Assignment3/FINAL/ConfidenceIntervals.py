from numpy import mean, var, sqrt, array, zeros, std
from Elevator import Elevator 

class ConfidenceIntervals: 

    def __init__(self, WaitingTime, PeopleInTheElevator, noEnteryLimitOfTheElevator, nrRuns, nrElevators, fraction5):
        """
        Initializing the confidence class and defining the attributes.
        """
        self.WaitingTime = WaitingTime
        self.PeopleInTheElevator = PeopleInTheElevator
        self.noEnteryLimitOfTheElevator = noEnteryLimitOfTheElevator
        self.nrRuns = nrRuns
        self.nrElevators = nrElevators
        self.fraction5 = fraction5
        

    def getCIWaitingTime(self):
        """ 
        Calculating the confidence intervals for the waiting time.
        Returns: Confidence Intervals, Mean and standard derivation.  
        """
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
        """
        Calculating the confidence intervals of the mean of people in the elevator.
        Returns: Confidence Intervals, Mean and standard derivation.  
        """
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
        """
        Calculating the confidence intervals of the probability of not entering the elevator due to capacity limits. 
        Returns: Confidence Intervals, Mean and standard derivation.  
        """
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
        """
        Calculating the confidence intervals of the fraction of people waiting longer than 5 minutes. 
        Returns: Confidence Intervals, Mean and standard derivation.  
        """
        confidenceIntervals =[0,0]
        confidenceIntervals[0] = mean(self.fraction5) - 1.96*sqrt(var(self.fraction5)/self.nrRuns)
        confidenceIntervals[1] = mean(self.fraction5) + 1.96*sqrt(var(self.fraction5)/self.nrRuns)
        means = mean(self.fraction5)
        standardDerivative = std(self.fraction5)
        return confidenceIntervals, means, standardDerivative 
    

    def __str__(self):
        """
        Returns string with the calculated confidence intervals, mean and standard deviation.
        """
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
            strWaitingTime += ("Floor " + str(i) + ": [" +str(round(cIWaitingTime[0][i][0],4)) + " , " + str(round(cIWaitingTime[1][i],4)) + " , " + str(round(cIWaitingTime[0][i][1],4)) + " ] Standard Derivation: " + str(round(cIWaitingTime[2][i],4)) + "\n")
            strProbabilityNoEntry += ("Floor "+ str(i) +": " + "[ " + str(round(cIProbabilityNoEntry[0][i][0],10)) + " , " + str(round(cIProbabilityNoEntry[1][i],10)) + " , " + str(round(cIProbabilityNoEntry[0][i][1],10)) + " ] Standard Derivation: " + str(round(cIProbabilityNoEntry[2][i],4)) + "\n")
        return ("Confidence Intervals of the mean waiting time: " + "\n" + 
                strWaitingTime +
                "Confidence Intervals of the  number of people in the elevators: " + "\n" +
                strElevator +
                "Confidence Intervals of the probability of users not entering due to capacity limitation: " + "\n" +
                strProbabilityNoEntry + "\n" +
                "Fraction of people are waiting longer than 5 minutes: " + "\n" +
                "[ " + str(round(cIfraction5[0][0],4)) + ", " + str(round(cIfraction5[1],4)) + ", " + str(round(cIfraction5[0][1],4)) + " ] Standard Derivation: " + str(round(cIfraction5[2],4)) ) 
     