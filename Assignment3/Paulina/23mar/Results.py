class Results:
    ''' Calculated the results.'''

    def __init__(self):
        self.sumWaitingTime = 1
        self.sumPeopleInTheElevator = 10 
        self.oldTime = 1 
        self.noEnteryLimitOfTheElevator = 5 
        self.allPeople = 20 

    def getMeanWaitingTime(self):
        return self.sumWaitingTime / self.oldTime 
    
    def getMeanOfPeopleInTheElevator(self):
        return self.sumPeopleInTheElevator / self.oldTime 

    def getProbabilityNoEntery(self):
        return self.noEnteryLimitOfTheElevator / self.allPeople
    
    def __str__(self):
        #st = ("Waiting time ", "people in the elevator ", "probability that a person cann't get into the elevator ")
        return ("Mean waiting time: " + str(self.getMeanWaitingTime()) + "\n" 
                + "mean of People in the Elevator: " + str(self.getMeanOfPeopleInTheElevator())+ "\n" 
                + "probability to not to enter the elevator because if the limit: " + str(self.getProbabilityNoEntery()))
    

#print(Results())