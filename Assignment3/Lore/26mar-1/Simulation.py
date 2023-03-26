from Customer import Customer
from Elevator import Elevator
from Distribution import Distribution
# from FCFSQueue import FCFSQueue
from scipy import stats
from collections import deque
from Results import Results
from numpy import *
from Event import Event 
from FES import FES 
import random

class Simulation:
    ''' Describes the simulation '''
    def __init__(self, arrDist, doorDist, nrElevators): #, arrDist1, arrDist2, arrDist3, arrDist4, doorDist, nrElevators):
        self.arrDist = arrDist
        self.doorDist = doorDist
        self.nrElevators = nrElevators
        self.probFloor = probFloor 


    def simulate(self, T):
        fes = FES()
        res = Results()
        elevator = [Elevator(elev) for elev in range(self.nrElevators)] # creates elevator for amount of elevators
        queueFloor = [deque() for floor in range(Elevator.FLOORS)] # makes a queue for each floor
        queueElevator = [deque() for elev in range(self.nrElevators)]  # makes a queue for each elevator 
        firstCustomerArrivalTime = 100000
        for floor in range(Elevator.FLOORS):
            firstArrivalTime = self.arrDist[floor].rvs()  # samples number of the next arrival 
            print("first arrival for floor", floor, "at time", firstArrivalTime)
            firstArrivalEvent = Event(Event.ARRIVAL, firstArrivalTime, floor)  # schedule first event 
            fes.add(firstArrivalEvent) # adding first event to future events 
            if firstCustomerArrivalTime > firstArrivalTime:
                firstCustomerArrivalTime = firstArrivalTime
        firstElevatorEvent = Event(Event.ELEVATORSTOPS, firstCustomerArrivalTime)
        print("elevator starts at floor 0 at time", firstCustomerArrivalTime)
        fes.add(firstElevatorEvent)
    
        
        round=0
        t = 0
        while t<T: 
            print("  ")
            print("round", round)
            round += 1
            e = fes.next()  # taking first element of the fes list and deleting this event 
            t = e.time

            if e.type == Event.ELEVATORSTOPS:
                for elev_i in range(nrElevators):
                    f = elevator[elev_i].floornumber
                    print("elevator number",elev_i,"stops at floor",elevator[elev_i].floornumber, "at time",t, "with direction upwards is", elevator[elev_i].directionUp)
                    if len(queueElevator[elev_i]) > 0 or len(queueFloor[f]) > 0: 
                        removeCustomers = []
                        for customer_elevator in queueElevator[elev_i]: 
                            if customer_elevator.destinationFloor == f: 
                                removeCustomers.append(customer_elevator)
                        addCustomers = []
                        for customer_floor in queueFloor[f]:
                            if customer_floor.directionUp == elevator[elev_i].directionUp:
                                addCustomers.append(customer_floor)
                        if len(removeCustomers) > 0 or len(addCustomers) > 0:
                            t += self.doorDist.rvs()
                            print("elevator doors opened at time",t)
                            for k in removeCustomers:
                                queueElevator[elev_i].remove(k)
                                t += 1     
                            print(len(removeCustomers),"customers left elevator at time", t)            
                            
                            if len(queueElevator[elev_i]) < elevator[elev_i].MAXPEOPLE:
                                customersThatGotInTheElevator = 0
                                customerThatWantInTheElevator = len(addCustomers) 
                                while len(addCustomers) > 0 and len(queueElevator[elev_i]) < elevator[elev_i].MAXPEOPLE:
                                    customersThatGotInTheElevator += 1
                                    print(addCustomers[0])
                                    queueElevator[elev_i].append(addCustomers[0])
                                    queueFloor[f].remove(addCustomers[0])
                                    t += 1
                                    res.sumWaitingTime += t - addCustomers[0].arrivalTime
                                    addCustomers.remove(addCustomers[0])
                                res.noEnteryLimitOfTheElevator +=  customerThatWantInTheElevator - customersThatGotInTheElevator
                            print(customersThatGotInTheElevator, "customers got in the elvator at time", t)
                            res.sumPeopleInTheElevator += len(queueElevator[elev_i])                
                            t += self.doorDist.rvs()
                            print("elevator doors closed at time",t)                            
                    print("elevator leaves with", len(queueElevator[elev_i]), "customers inside the elevator")  
                    Elevator.newFloor(elevator[elev_i]) # change the floor of the elevator to the next one and if needed change direction
                    nextFloor = Event(Event.ELEVATORSTOPS, t+Elevator.MOVETIME)
                    fes.add(nextFloor)
                
                
            if e.type == Event.ARRIVAL: # arrival of a customer
                des = random.choices(range(Elevator.FLOORS), weights = probFloor[e.floor], k = 1)[0] 
                c = Customer(t, des, e.floor)
                res.allPeople += 1
                queueFloor[e.floor].append(c)
                print(c)
                a = self.arrDist[e.floor].rvs() 
                nextCustomer = Event(Event.ARRIVAL, t+a, e.floor)
                fes.add(nextCustomer)   

        # checks that no users are left in the elevator or waiting in front of the elevators 
        # TODO !!!!!!! update part below !!!!!!!!
        restEvents = len(fes.events) 
        for peopleWaitingOrInElevator in range(restEvents):
            print(peopleWaitingOrInElevator)
            e = fes.next()
            if e.type == Event.ELEVATORSTOPS:
                f = elevator[0].floornumber
                if len(queueElevator[0]) > 0 or len(queueFloor[f]) > 0:
                    t += self.doorDist.rvs()
                    removeCustomers = []
                    for customer_i in queueElevator[0]:  # CHANGED: [0] to the number of the elevator. 
                        print("customer", customer_i)
                        if customer_i.destinationFloor == f: 
                            removeCustomers.append(customer_i)
                            print("the i^th customer: ", customer_i)
                    for k in removeCustomers:
                        queueElevator[0].remove(k)
                    t += 1     

                    if len(queueElevator[0]) < elevator[0].MAXPEOPLE:
                        for a in arange(Elevator.FLOORS):
                            if a == f:
                                print("right floor", "a", a, "f", f)
                                print("len q", len(queueFloor[a]))
                                customersThatGotInTheElevator = 0
                                customerThatWantInTheElevator = len(queueFloor[a])
                                while len(queueFloor[a]) > 0 and len(queueElevator[0]) < elevator[0].MAXPEOPLE:
                                    customersThatGotInTheElevator += 1
                                    print("only if queue")
                                    c = queueFloor[a][0]
                                    queueElevator[0].append(c)
                                    res.sumWaitingTime += t - c.arrivalTime
                                    print("waitingtime: ", res.sumWaitingTime, t)
                                    t += 1
                                    queueFloor[a].remove(c)
                                print("hallo",len(queueFloor[a]), customersThatGotInTheElevator)
                                res.noEnteryLimitOfTheElevator +=  customerThatWantInTheElevator - customersThatGotInTheElevator
                                print(res.noEnteryLimitOfTheElevator)
                    print(len(queueElevator[0]))
                    res.sumPeopleInTheElevator += len(queueElevator[0])                
                    t += self.doorDist.rvs()                            
                print("t end", t)  
                if elevator[0].floornumber == 1:
                    elevator[0].floornumber -= 1
                else: 
                    elevator[0].floornumber += 1
                nextFloor = Event(Event.ELEVATORSTOPS, t+Elevator.MOVETIME)
                fes.add(nextFloor)
        res.totalTime = t 
        # print(res)                       

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

nrElevators = 1 # amount of elevators

sim = Simulation(arrDist, doorDist, nrElevators)

sim.simulate(200)
