from Customer import Customer
from Elevator import Elevator
from Distribution import Distribution
from ConfidenceIntervals import ConfidenceIntervals
from scipy import stats
from collections import deque
from Results import Results
from numpy import *
from Event import Event 
from FES import FES 
import random, time


class Simulation:
    ''' Describes the simulation '''

    def __init__(self, arrDist, doorDist, nrElevators, probFloor, impatienceDown = None, impatienceUp = None, question6 = False):
        ''' Initialise the simulation input'''
        self.arrDist = arrDist
        self.doorDist = doorDist
        self.nrElevators = nrElevators
        self.probFloor = probFloor 
        self.impatienceDown = impatienceDown
        self.impatienceUp = impatienceUp
        self.question6 = question6


    def simulate(self, T, timeUnitsThatAreDeleted):
        ''' Perform the simulation '''
        fes = FES()
        res = Results(self.nrElevators,timeUnitsThatAreDeleted)

        # make a queue for each floor
        queueFloor = [deque() for floor in range(Elevator.FLOORS)] 
        # make a queue for each elevator 
        queueElevator = [deque() for elev in range(self.nrElevators)]
        
        # add the first arrival event for customers to the FES for each floor
        firstCustomerArrivalTime = T # initialise the firstCustomerArrivalTime
        for floor in range(Elevator.FLOORS):
            firstArrivalTime = self.arrDist[floor].rvs()  # sample number of the next arrival 
            firstArrivalEvent = Event(Event.CUSTOMER_ARRIVAL, firstArrivalTime, floor = floor)
            fes.add(firstArrivalEvent) 
            # save the first arrival
            if firstCustomerArrivalTime > firstArrivalTime:
                firstCustomerArrivalTime = firstArrivalTime
        
        # add the first stop event for elevators to the FES for each elevator when the first customer arrives
        elevatorList = [] # initialise the elevatorList
        for elevator_i in arange(self.nrElevators):
            elevatorEvent = Event(Event.ELEVATOR_STOPS, firstCustomerArrivalTime, floor = 0, elevatorNr = elevator_i)
            fes.add(elevatorEvent)
            elevatorList.append(Elevator(firstCustomerArrivalTime, elevator_i, self.nrElevators , 0)) 

        t = 0 # initilise time
        custnr = 0 # initilise the customer number
        
        # perform the next event when the time is less or equal to the end time of the simulation
        while fes.checkNext().time <= T:
            e = fes.next()  # taking first event of the FES list and deleting this event 
            t = e.time

            # Elevator reaches a certain floor
            if e.type == Event.ELEVATOR_STOPS:
                elevator_i = elevatorList[e.elevatorNr]
                # If there are people inside the elevator or in the queue of the floor it stops at, check if people want to get in or out of the elevator
                if len(queueElevator[e.elevatorNr]) > 0 or len(queueFloor[elevator_i.floornumber]) > 0: 
                    removeCustomers = Elevator.checkLeaving(elevatorList[e.elevatorNr], queueElevator[e.elevatorNr])
                    addCustomers = Elevator.checkEntering(elevatorList[e.elevatorNr], queueFloor[elevatorList[e.elevatorNr].floornumber]) 
                    # Open doors when people want to get in (only if maximum capacity is not reached yet) or out of the elevator
                    if len(removeCustomers) > 0 or (len(addCustomers) > 0 and len(queueElevator[e.elevatorNr]) < Elevator.MAXPEOPLE):
                        OpenDoors = Event(Event.ELEVATOR_OPEN_DOORS, t, elevatorNr = e.elevatorNr, floor = elevator_i.floornumber)
                        fes.add(OpenDoors)
                    # Go to the next floor without opening its doors if all customers inside the elevator stays the same
                    else:
                        Elevator.newFloor(elevator_i)
                        NextFloor = Event(Event.ELEVATOR_STOPS, t + Elevator.MOVETIME, elevatorNr=e.elevatorNr, floor = elevator_i.floornumber)
                        fes.add(NextFloor)
                # Go to the next floor without opening its doors if all customers inside the elevator stays the same
                else:
                    Elevator.newFloor(elevator_i)
                    NextFloor = Event(Event.ELEVATOR_STOPS, t + Elevator.MOVETIME, elevatorNr=e.elevatorNr, floor = elevator_i.floornumber)
                    fes.add(NextFloor)
            
            # Elevator opens its doors
            if e.type == Event.ELEVATOR_OPEN_DOORS:
                # Add the time it takes to open the doors
                t += self.doorDist.rvs()
                # Let a customer (FCFS policy) leave the elevator at the time the doors are opened, when people want to leave the elevator
                removeCustomers = Elevator.checkLeaving(elevatorList[e.elevatorNr], queueElevator[e.elevatorNr])
                if len(removeCustomers) > 0:
                    FirstCustomerLeaves = Event(Event.CUSTOMER_LEAVE, t, customer = removeCustomers[0], elevatorNr = e.elevatorNr)
                    fes.add(FirstCustomerLeaves)
                # When no people leave the elevator: Let a customer (FCFS policy) enter the elevator at the time the doors are opened, when people want to enter the elevator
                else:      
                    addCustomers = Elevator.checkEntering(elevatorList[e.elevatorNr], queueFloor[elevatorList[e.elevatorNr].floornumber])
                    if len(addCustomers) > 0 and len(queueElevator[e.elevatorNr]) < Elevator.MAXPEOPLE:
                        FirstCustomerEnters = Event(Event.CUSTOMER_ENTER, t, customer = addCustomers[0], elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                        fes.add(FirstCustomerEnters)
                    # If nobody wants to leave or enter the elevator close the doors of the elevator at the time the doors are opened
                    else:
                        CloseDoors = Event(Event.ELEVATOR_CLOSE_DOORS, t, elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                        fes.add(CloseDoors)

            # Customer leaves the elevator
            if e.type == Event.CUSTOMER_LEAVE:
                # Add the time it takes to let a person leave the elevator
                t += Customer.MOVETIME
                # Remove the customer from the elevator
                queueElevator[e.elevatorNr].remove(e.customer)
                # Register the time, the elevator number and the amount of people inside the elevator after the warmup time 
                if t > timeUnitsThatAreDeleted:
                    res.registerPeopleInElevator(t, len(queueElevator[e.elevatorNr]), e.elevatorNr)
                # If there are still people who want to leave the elevator at this floor, let them leave (FCFS policy)
                removeCustomers = Elevator.checkLeaving(elevatorList[e.elevatorNr], queueElevator[e.elevatorNr])
                if len(removeCustomers) > 0:
                    CustomerLeaves = Event(Event.CUSTOMER_LEAVE, t, customer = removeCustomers[0], elevatorNr = e.elevatorNr)
                    fes.add(CustomerLeaves)
                # If nobody wants to leave the elevator, let people enter the elevator (FCFS policy)
                else:
                    addCustomers = Elevator.checkEntering(elevatorList[e.elevatorNr], queueFloor[elevatorList[e.elevatorNr].floornumber])
                    if len(addCustomers) > 0 and len(queueElevator[e.elevatorNr]) < Elevator.MAXPEOPLE:
                        FirstCustomerEnters = Event(Event.CUSTOMER_ENTER, t, customer = addCustomers[0], elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                        fes.add(FirstCustomerEnters)
                    # If nobody wants to leave or enter the elevator, close the elevator doors
                    else:
                        CloseDoors = Event(Event.ELEVATOR_CLOSE_DOORS, t, elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                        fes.add(CloseDoors)

            # Customer enters the elevator
            if e.type == Event.CUSTOMER_ENTER:
                # Customer can only enter if it is in the same floor as the elevator
                if e.customer in queueFloor[elevatorList[e.elevatorNr].floornumber]:
                    # Register the waiting time after the warmup time
                    if t > timeUnitsThatAreDeleted:
                        res.sumWaitingTime[elevatorList[e.elevatorNr].floornumber] += t - e.customer.arrivalTime
                        res.customersEnter += 1
                        # Register is the customer waited for longer than 5 minutes (300 secs) after the warmup time
                        if (t - e.customer.arrivalTime) > 300:
                            res.customerLongerThan5 += 1
                    # Add the time it takes to let a person enter the elevator
                    t += Customer.MOVETIME
                    # Remove the customer from the queue and add the customer to the elevator
                    queueFloor[elevatorList[e.elevatorNr].floornumber].remove(e.customer)
                    queueElevator[e.elevatorNr].append(e.customer)
                    # Register the time, the elevator number and the amount of people inside the elevator and add an entering customer after the warmup time 
                    if t > timeUnitsThatAreDeleted:
                        res.registerPeopleInElevator(t, len(queueElevator[e.elevatorNr]), e.elevatorNr)
                        res.enterCustomer[elevatorList[e.elevatorNr].floornumber] +=1
                # If there are still people who want to enter the elevator, let them enter (FCFS policy)
                addCustomers = Elevator.checkEntering(elevatorList[e.elevatorNr], queueFloor[elevatorList[e.elevatorNr].floornumber])
                if len(addCustomers) > 0 and len(queueElevator[e.elevatorNr]) < Elevator.MAXPEOPLE:
                    FirstCustomerEnters = Event(Event.CUSTOMER_ENTER, t, customer = addCustomers[0], elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                    fes.add(FirstCustomerEnters)
                # If nobody wants to enter the elevator or the maximum capacity is reached, close the elevator doors
                else:
                    CloseDoors = Event(Event.ELEVATOR_CLOSE_DOORS, t, elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                    fes.add(CloseDoors)
                    # Add the amount off customers that are left waiting when maximum capacity is reached after warmup time
                    if t > timeUnitsThatAreDeleted:
                        if len(addCustomers) > 0:
                            res.waitedCustomer[elevatorList[e.elevatorNr].floornumber] += len(addCustomers)
                                       
            # Elevator opens its doors
            if e.type == Event.ELEVATOR_CLOSE_DOORS:
                # Add the time it takes to close the doors
                t += self.doorDist.rvs()
                # Let the elevator go to the next floor when the doors are closed
                Elevator.newFloor(elevatorList[e.elevatorNr])
                NextFloor = Event(Event.ELEVATOR_STOPS, t + Elevator.MOVETIME, elevatorNr=e.elevatorNr, floor = elevator_i.floornumber)
                fes.add(NextFloor) 

            # Customers arrives at the queue
            if e.type == Event.CUSTOMER_ARRIVAL: 
                # Add one to the customer number
                custnr += 1
                # Add one to the all customers at a certain floor after the warmup time
                if t > timeUnitsThatAreDeleted:
                    res.allPeople[e.floor] += 1
                # Get the destinationfloor of the customer and append the customer to the queue
                des = random.choices(range(Elevator.FLOORS), weights = probFloor[e.floor], k = 1)[0] 
                c = Customer(t, des, e.floor,custnr)
                queueFloor[e.floor].append(c)
                # Get the time it takes a customer to leave the queue before entering the elevator due to impatience if the extension is applied
                if self.question6:
                    impatienceTime = c.impatience(self.impatienceDown, self.impatienceUp)
                    # Add the event of the customer leaving the queue after the impatience time
                    impatientCustomer = Event(Event.CUSTOMER_IMPATIENT, t + impatienceTime, floor = e.floor, customer=c)
                    fes.add(impatientCustomer)
                # Schedule the next time a customer arrives the floor
                InterArrivalTime = self.arrDist[e.floor].rvs() 
                nextCustomer = Event(Event.CUSTOMER_ARRIVAL, t+InterArrivalTime, floor = e.floor)
                fes.add(nextCustomer)

            # Impatient customer leaves the queue
            if e.type == Event.CUSTOMER_IMPATIENT:
                # If the customer is still in the queue after the impatience time, remove the customer from the queue
                if e.customer in queueFloor[e.floor]:
                    queueFloor[e.floor].remove(e.customer)


        # Register the total time of the simulation after the warmup time
        res.totalTime = t - timeUnitsThatAreDeleted

        # Return the results
        return res 
           
''' input for different secarios of the simulation '''
nrElevators = 5 # amount of elevators, vary this number

probFloor = array([[0, 0.1, 0.3, 0.4, 0.2],
             [0.7, 0, 0.1, 0.1, 0.1],
             [0.6, 0.2, 0, 0.1, 0.1],
             [0.6, 0.2, 0.1, 0, 0.1],
             [0.5, 0.2, 0.2, 0.1, 0]])
arrDist0 = Distribution(stats.expon(scale = 60/13.1))
arrDist1 = Distribution(stats.expon(scale = 60/3.4))
arrDist2 = Distribution(stats.expon(scale = 60/2.1))
arrDist3 = Distribution(stats.expon(scale = 60/9.2))
arrDist4 = Distribution(stats.expon(scale = 60/8.8))

arrDist = [arrDist0, arrDist1, arrDist2, arrDist2, arrDist3, arrDist4]
doorDist = Distribution(stats.expon(scale = 3))

probFloorQ5 = array([[0, 0.1, 0.3, 0.4, 0.2],
             [0, 0, 1/3, 1/3, 1/3],
             [0, 0, 0, 0.5, 0.5],
             [0.6, 0.2, 0.1, 0, 0.1],
             [0.5, 0.2, 0.2, 0.1, 0]])
arrDist1Q5 = Distribution(stats.expon(scale = 60/(3.4*0.3)))
arrDist2Q5 = Distribution(stats.expon(scale = 60/(2.1*0.2)))
arrDistQ5 = [arrDist0, arrDist1, arrDist2, arrDist2, arrDist3, arrDist4]

impatienceDown = [0, 60, 90, 120, 150] # seconds before customer takes stairs for amount of floors downstairs
impatienceUp = [0, 90, 180, 240, 300] # seconds before customer takes stairs for amount of floors upstairs

''' different secarios of the simulation '''
sim = Simulation(arrDist, doorDist, nrElevators, probFloor)
# sim = Simulation(arrDistQ5, doorDist, nrElevators, probFloorQ5) # for question 5
# sim = Simulation(arrDist, doorDist, nrElevators, probFloor ,impatienceDown, impatienceUp, question6=True) # for question 6

''' input for the results and confidence intervals '''
timeUnitsThatAreDeleted = 5000  #time that is not taken into account for the results   
nrRuns = 235
WaitingTime = list(zeros(nrRuns))
PeopleInTheElevator = list(zeros(nrRuns))
noEnteryLimitOfTheElevator = list(zeros(nrRuns))
fraction5 = list(zeros(nrRuns))

for i in range(nrRuns): 
    start = time.time()
    results  = sim.simulate(50_000, timeUnitsThatAreDeleted) 
    end = time.time()
    print("time: ",end-start)
    WaitingTime[i] = results.getMeanWaitingTime()
    PeopleInTheElevator[i] = results.getMeanOfPeopleInTheElevator()
    noEnteryLimitOfTheElevator[i] = results.getProbabilityNoEntery()
    fraction5[i] = results.fractionLongerThan5()

cI = ConfidenceIntervals(WaitingTime, PeopleInTheElevator, noEnteryLimitOfTheElevator, nrRuns, nrElevators, fraction5)

print(cI)