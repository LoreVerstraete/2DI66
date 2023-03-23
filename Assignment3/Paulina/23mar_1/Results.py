class Results:
    ''' Calculated the results.'''

    def __init__(self):
        self.sumWaitingTime = 0
        self.sumPeopleInTheElevator = 0 
        self.totalTime = 1
        self.noEnteryLimitOfTheElevator = 0 
        self.allPeople = 1 

    def getMeanWaitingTime(self):
        return self.sumWaitingTime / self.totalTime
    
    def getMeanOfPeopleInTheElevator(self):
        return self.sumPeopleInTheElevator / self.totalTime 

    def getProbabilityNoEntery(self):
        return self.noEnteryLimitOfTheElevator / self.allPeople
    
    def __str__(self):
        #st = ("Waiting time ", "people in the elevator ", "probability that a person cann't get into the elevator ")
        return ("Mean waiting time: " + str(self.getMeanWaitingTime()) + "\n" 
                + "mean of People in the Elevator: " + str(self.getMeanOfPeopleInTheElevator())+ "\n" 
                + "probability to not to enter the elevator because if the limit: " + str(self.getProbabilityNoEntery()))
    

print(Results())