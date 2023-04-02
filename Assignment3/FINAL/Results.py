from Elevator import Elevator
from numpy import zeros, array

class Results:
    ''' 
    Class to calculate the results.
    '''

    def __init__(self, numbersOfAllElevators, timeUnitsDeleted):
        """
        Initializing the results class and defining the attibutes of the class. 
        """
        self.sumWaitingTime = zeros(Elevator.FLOORS)
        self.sumPeopleInTheElevator = zeros(numbersOfAllElevators)
        self.totalTime = 0
        self.allPeople = zeros(Elevator.FLOORS)   
        self.oldTime = array([timeUnitsDeleted] *numbersOfAllElevators)
        timeUnitsDeleted
        self.numbersOfAllElevators = numbersOfAllElevators
        self.enterCustomer = zeros(Elevator.FLOORS)
        self.waitedCustomer = zeros(Elevator.FLOORS)
        self.customerLongerThan5 = 0
        self.customersEnter = 0 

    def getMeanWaitingTime(self):
        """ 
        Calculating the mean waiting time. 
        Dividing the sum of the waiting time of all people by the number of all people that used the elevator. 
        Returns: mean waiting time.    
        """
        return self.sumWaitingTime / self.allPeople
    
    def registerPeopleInElevator(self, t, peopleInElevator, nrElevator):
        """
        Calculating the normalised number of people in the elevator.
        Multipling the number of people in the elevator by the time they are in the elevator. 
        """
        self.sumPeopleInTheElevator[nrElevator] += peopleInElevator*(t-self.oldTime[nrElevator])
        self.oldTime[nrElevator] = t
        
    def getMeanOfPeopleInTheElevator(self):
        """
        Calculating the mean of peopel in the elevator. 
        Dividing the normalized sum of prople in the elevator by the total time. 
        Returns: mean waiting time of the people in the elevator. 
        """
        return self.sumPeopleInTheElevator / self.totalTime

    def getProbabilityNoEntery(self):
        """
        Calculating the probability of not entering the elevator because of capacity limitations. 
        Dividing the waiting customers by the number of customers entering and customers waiting. 
        Returns: Probability of not entering the elevator.
        """
        return self.waitedCustomer / (self.enterCustomer + self.waitedCustomer)
    
    def fractionLongerThan5(self):
        """
        Calculating the fraction of users that are waiting longer than 5 minutes. 
        Dividing the number of users that waited longer than 5 minutes by the number of all users. 
        Returns: fractions of users waiting longer than 5 minutes. 
        """
        return self.customerLongerThan5 / self.customersEnter #sum(self.allPeople)

    
    def __str__(self):
        """
        Returns string with the calculated mean waiting time, mean of the peopel in the elevator, the probability of not entering and the mean and standard deviation.
        """
        return ("Mean waiting time: " + str(self.getMeanWaitingTime()) + "\n" 
                + "mean of People in the Elevator: " + str(self.getMeanOfPeopleInTheElevator())+ "\n" 
                + "probability to not to enter the elevator because if the limit: " + str(self.getProbabilityNoEntery()) + "\n"
                + "Total number of customers: " + str(self.allPeople) + "\n" 
                + "fraction of people waiting longer than 5 minutes: " + str(self.fractionLongerThan5()) + "\n"
                + "Total run time: " + str(self.totalTime))
    
