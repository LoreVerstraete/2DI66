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

#TODO: leave first events out 


class Simulation:
    ''' Describes the simulation '''
    def __init__(self, arrDist, doorDist, nrElevators, probFloor, impatienceDown = None, impatienceUp = None, question6 = False):
        self.arrDist = arrDist
        self.doorDist = doorDist
        self.nrElevators = nrElevators
        self.probFloor = probFloor 
        self.impatienceDown = impatienceDown
        self.impatienceUp = impatienceUp
        self.question6 = question6
        self.show_queues = False
        self.show_addremove = False
        self.show_otherprints = False
        self.show_res = False


    def simulate(self, T, timeUnitsThatAreDeleted):
        # initialize simulation
        fes = FES()
        res = Results(self.nrElevators)
        queueFloor = [deque() for floor in range(Elevator.FLOORS)] # makes a queue for each floor
        queueElevator = [deque() for elev in range(self.nrElevators)]  # makes a queue for each elevator 
        firstCustomerArrivalTime = T
        
        for floor in range(Elevator.FLOORS):
            firstArrivalTime = self.arrDist[floor].rvs()  # samples number of the next arrival 
            firstArrivalEvent = Event(Event.CUSTOMER_ARRIVAL, firstArrivalTime, floor = floor)  # schedule first event 
            fes.add(firstArrivalEvent) # adding first event to future events 
            if firstCustomerArrivalTime > firstArrivalTime:
                firstCustomerArrivalTime = firstArrivalTime
        
        elevatorList = []
        for elevator_i in arange(self.nrElevators):
            elevatorEvent = Event(Event.ELEVATOR_STOPS, firstCustomerArrivalTime, floor = 0, elevatorNr = elevator_i)
            fes.add(elevatorEvent)
            elevatorList.append(Elevator(firstCustomerArrivalTime, self.nrElevators , elevator_i, 0))
        
        t = 0
        custnr = 0
        
        while fes.checkNext().time <= T:
            e = fes.next()  # taking first element of the fes list and deleting this event 
            t = e.time

            if e.type == Event.ELEVATOR_STOPS:
                # print(e)
                elevator_i = elevatorList[e.elevatorNr]
                if len(queueElevator[e.elevatorNr]) > 0 or len(queueFloor[elevator_i.floornumber]) > 0: 
                    removeCustomers = Elevator.checkLeaving(elevatorList[e.elevatorNr], queueElevator[e.elevatorNr])
                    addCustomers = Elevator.checkEntering(elevatorList[e.elevatorNr], queueFloor[elevatorList[e.elevatorNr].floornumber]) 
                    #print("     ",len(queueElevator[e.elevatorNr]), "customers in elevator", e.elevatorNr,"           ",len(removeCustomers), "customers should be removed from the elevator at floor",elevator_i.floornumber) 
                    #print("     ",len(queueFloor[elevator_i.floornumber]), "customers in queue at floor",elevator_i.floornumber,"     ",len(addCustomers), "customers should be added to the elevator at floor",elevator_i.floornumber)     
                    if len(removeCustomers) > 0 or len(addCustomers) > 0:
                        OpenDoors = Event(Event.ELEVATOR_OPEN_DOORS, t, elevatorNr = e.elevatorNr, floor = elevator_i.floornumber)
                        fes.add(OpenDoors)
                    else:
                        Elevator.newFloor(elevator_i)
                        NextFloor = Event(Event.ELEVATOR_STOPS, t + Elevator.MOVETIME, elevatorNr=e.elevatorNr, floor = elevator_i.floornumber)
                        fes.add(NextFloor)
                else:
                    Elevator.newFloor(elevator_i)
                    NextFloor = Event(Event.ELEVATOR_STOPS, t + Elevator.MOVETIME, elevatorNr=e.elevatorNr, floor = elevator_i.floornumber)
                    fes.add(NextFloor)
                
            if e.type == Event.ELEVATOR_OPEN_DOORS:
                t += self.doorDist.rvs()
                # print(e,", doors are fully opened at time", t)
                #print(e.floor)
                #print(len(queueFloor[e.floor]))
                if t> timeUnitsThatAreDeleted:
                    res.peopleInThisFloor[e.floor] = len(queueFloor[e.floor])
                removeCustomers = Elevator.checkLeaving(elevatorList[e.elevatorNr], queueElevator[e.elevatorNr])
                if len(removeCustomers) > 0:
                    FirstCustomerLeaves = Event(Event.CUSTOMER_LEAVE, t, customer = removeCustomers[0], elevatorNr = e.elevatorNr)
                    fes.add(FirstCustomerLeaves)
                else:      
                    addCustomers = Elevator.checkEntering(elevatorList[e.elevatorNr], queueFloor[elevatorList[e.elevatorNr].floornumber])
                    if len(addCustomers) > 0 and len(queueElevator[e.elevatorNr]) < Elevator.MAXPEOPLE:
                        FirstCustomerEnters = Event(Event.CUSTOMER_ENTER, t, customer = addCustomers[0], elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                        fes.add(FirstCustomerEnters)
                    else:
                        CloseDoors = Event(Event.ELEVATOR_CLOSE_DOORS, t, elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                        fes.add(CloseDoors)
                        # if len(addCustomers) > 0:
                        #     res.noEnteryLimitOfTheElevator[elevatorList[e.elevatorNr].floornumber] +=1
                        #     print("no entery", res.noEnteryLimitOfTheElevator)

            if e.type == Event.CUSTOMER_LEAVE:
                # print("     ",e)
                t += Customer.MOVETIME
                queueElevator[e.elevatorNr].remove(e.customer)
                if t > timeUnitsThatAreDeleted:
                    res.registerPeopleInElevator(t, len(queueElevator[e.elevatorNr]), e.elevatorNr)
                removeCustomers = Elevator.checkLeaving(elevatorList[e.elevatorNr], queueElevator[e.elevatorNr])
                if len(removeCustomers) > 0:
                    CustomerLeaves = Event(Event.CUSTOMER_LEAVE, t, customer = removeCustomers[0], elevatorNr = e.elevatorNr)
                    fes.add(CustomerLeaves)
                else:
                    addCustomers = Elevator.checkEntering(elevatorList[e.elevatorNr], queueFloor[elevatorList[e.elevatorNr].floornumber])
                    if len(addCustomers) > 0 and len(queueElevator[e.elevatorNr]) < Elevator.MAXPEOPLE:
                        FirstCustomerEnters = Event(Event.CUSTOMER_ENTER, t, customer = addCustomers[0], elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                        fes.add(FirstCustomerEnters)
                    else:
                        CloseDoors = Event(Event.ELEVATOR_CLOSE_DOORS, t, elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                        fes.add(CloseDoors)
                        # if len(addCustomers) > 0:
                        #     res.noEnteryLimitOfTheElevator[elevatorList[e.elevatorNr].floornumber] +=1
                        #     print("no entery", res.noEnteryLimitOfTheElevator)

            if e.type == Event.CUSTOMER_ENTER:
                if e.customer in queueFloor[elevatorList[e.elevatorNr].floornumber]:
                    # print("     ",e)
                    if t > timeUnitsThatAreDeleted:
                        res.sumWaitingTime[elevatorList[e.elevatorNr].floornumber] += t - e.customer.arrivalTime
                    t += Customer.MOVETIME
                    queueFloor[elevatorList[e.elevatorNr].floornumber].remove(e.customer)
                    queueElevator[e.elevatorNr].append(e.customer)
                    res.newPeopleInTheElevator[e.elevatorNr] += 1
                    if t > timeUnitsThatAreDeleted:
                        res.registerPeopleInElevator(t, len(queueElevator[e.elevatorNr]), e.elevatorNr)
                addCustomers = Elevator.checkEntering(elevatorList[e.elevatorNr], queueFloor[elevatorList[e.elevatorNr].floornumber])
                if len(addCustomers) > 0 and len(queueElevator[e.elevatorNr]) < Elevator.MAXPEOPLE:
                    FirstCustomerEnters = Event(Event.CUSTOMER_ENTER, t, customer = addCustomers[0], elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                    fes.add(FirstCustomerEnters)
                else:
                    CloseDoors = Event(Event.ELEVATOR_CLOSE_DOORS, t, elevatorNr = e.elevatorNr, floor = elevatorList[e.elevatorNr].floornumber)
                    fes.add(CloseDoors)
                    if len(addCustomers) > 0:
                        res.noEnteryLimitOfTheElevator[elevatorList[e.elevatorNr].floornumber] +=1
                        # print("no entery", res.noEnteryLimitOfTheElevator)

            if e.type == Event.ELEVATOR_CLOSE_DOORS:
                # print(e)
                # print(e.floor)
                res.numberDoorCloses[e.floor] += 1
                # print(res.numberDoorCloses)
                # print(queueFloor[e.floor])
                # if len(queueFloor[e.floor])>0:
                #     #floorlist = [ elevatorList[e.elevatorNr].floornumber for i in elevatorList]  
                #     #if floorlist.count(elevatorList[e.elevatorNr].floornumber) == 1: #checks if there is only one elevator at this floor 
                #         if t > timeUnitsThatAreDeleted:
                #             # res.noEnteryLimitOfTheElevator[e.floor] += (len(queueFloor[e.floor]) - res.newPeopleInTheElevator[e.elevatorNr])/len(queueFloor[e.floor]) 
                #             res.noEnteryLimitOfTheElevator[e.floor] += 1
                #             print(res.noEnteryLimitOfTheElevator)
                #             print("prob: ",res.noEnteryLimitOfTheElevator[e.floor], " floor ", e.floor)
                t += self.doorDist.rvs()
                Elevator.newFloor(elevatorList[e.elevatorNr])
                NextFloor = Event(Event.ELEVATOR_STOPS, t + Elevator.MOVETIME, elevatorNr=e.elevatorNr, floor = elevator_i.floornumber)
                fes.add(NextFloor)
                res.newPeopleInTheElevator[e.elevatorNr] = 0 # after a change of floors for this elevator the number of customers that are new in the elevators are set to zero. 
                if t > timeUnitsThatAreDeleted:
                    res.numberofTimesElevatorIsInNewFloor[e.elevatorNr] += 1
                    # print("moved elevators: ", res.numberofTimesElevatorIsInNewFloor)

            if e.type == Event.CUSTOMER_ARRIVAL: # arrival of a customer
                ########## add customer number
                custnr += 1
                if t > timeUnitsThatAreDeleted:
                    res.allPeople[e.floor] += 1
                des = random.choices(range(Elevator.FLOORS), weights = probFloor[e.floor], k = 1)[0] 
                # c = Customer(t, des, e.floor,res.allPeople)
                # change line above to:
                c = Customer(t, des, e.floor,custnr)
                queueFloor[e.floor].append(c)                
                if self.question6:
                    impatienceTime = c.impatience(self.impatienceDown, self.impatienceUp)
                    impatientCustomer = Event(Event.CUSTOMER_IMPATIENT, t + impatienceTime, floor = e.floor, customer=c)
                    fes.add(impatientCustomer)
                InterArrivalTime = self.arrDist[e.floor].rvs() 
                nextCustomer = Event(Event.CUSTOMER_ARRIVAL, t+InterArrivalTime, floor = e.floor)
                fes.add(nextCustomer)
                #print("          ","\033[95m{}\033[0m".format(c))  

            if e.type == Event.CUSTOMER_IMPATIENT:
                if e.customer in queueFloor[e.floor]:
                    queueFloor[e.floor].remove(e.customer)
                    #print("          ","\033[94m{}\033[0m".format(e))


        res.totalTime = t - timeUnitsThatAreDeleted
        return res 
           

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

nrElevators = 1 # amount of elevators, vary this number

impatienceDown = [0, 10, 20, 40, 60] # seconds before customer takes stairs for amount of floors downstairs
impatienceUp = [0, 30, 60, 100, 150] # seconds before customer takes stairs for amount of floors upstairs

sim = Simulation(arrDist, doorDist, nrElevators, probFloor)
# sim = Simulation(arrDistQ5, doorDist, nrElevators, probFloorQ5) # for question 5
# sim = Simulation(arrDist, doorDist, nrElevators, probFloor ,impatienceDown, impatienceUp, question6=True) # for question 6

# for the simulation:
timeUnitsThatAreDeleted = 10000  #time that is not taken into account for the results   
nrRuns = 5
WaitingTime = list(zeros(nrRuns))
PeopleInTheElevator = zeros(nrRuns)
noEnteryLimitOfTheElevator = list(zeros(nrRuns))

for i in range(nrRuns): 
    start = time.time()
    results  = sim.simulate(10_0000, timeUnitsThatAreDeleted)   #10_0000
    end = time.time()
    print("time: ",end-start)
    WaitingTime[i] = results.getMeanWaitingTime()
    PeopleInTheElevator[i] = results.getMeanOfPeopleInTheElevator()
    noEnteryLimitOfTheElevator[i] = results.getProbabilityNoEntery()

cI = ConfidenceIntervals(WaitingTime, PeopleInTheElevator, noEnteryLimitOfTheElevator, nrRuns)
# cI = ConfidenceIntervals(WaitingTime, PeopleInTheElevator, 1, nrRuns)
print("Time units Deleted", 10000)
print("nrRuns", nrRuns)
print("nrElevators", nrElevators)
print(cI)

