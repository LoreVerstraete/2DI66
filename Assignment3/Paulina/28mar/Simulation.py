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
    def __init__(self, arrDist, doorDist, nrElevators, probFloor, impatienceDown = None, impatienceUp = None, question6 = False):
        self.arrDist = arrDist
        self.doorDist = doorDist
        self.nrElevators = nrElevators
        self.probFloor = probFloor 
        self.impatienceDown = impatienceDown
        self.impatienceUp = impatienceUp
        self.question6 = question6
        self.show_queues = True
        self.show_addremove = False
        self.show_otherprints = True
        self.show_res = False


    def simulate(self, T):
        # initialize simulation
        fes = FES()
        res = Results()
        queueFloor = [deque() for floor in range(Elevator.FLOORS)] # makes a queue for each floor
        queueElevator = [deque() for elev in range(self.nrElevators)]  # makes a queue for each elevator 
        firstCustomerArrivalTime = T
        for floor in range(Elevator.FLOORS):
            firstArrivalTime = self.arrDist[floor].rvs()  # samples number of the next arrival 
            if self.show_otherprints:
                print("first arrival for floor", floor, "at time", firstArrivalTime)
            firstArrivalEvent = Event(Event.ARRIVAL, firstArrivalTime, floor)  # schedule first event 
            fes.add(firstArrivalEvent) # adding first event to future events 
            if firstCustomerArrivalTime > firstArrivalTime:
                firstCustomerArrivalTime = firstArrivalTime
        
        elevatorList = []
        for elevator_i in arange(self.nrElevators):
            elevatorEvent = Event(Event.ELEVATORSTOPS, firstCustomerArrivalTime, 0, elevator_i)
            fes.add(elevatorEvent)
            elevatorList.append(Elevator(firstCustomerArrivalTime, elevator_i, 0))
            if self.show_otherprints:
                print("elevator nr", elevator_i, "starts at floor 0 at time", firstCustomerArrivalTime)
        
        round=0
        t = 0
        #while t<T: 
        while fes.checkNext().time <= T:
            if self.show_otherprints:
                print("  ")
                print("round", round)
                round += 1
            e = fes.next()  # taking first element of the fes list and deleting this event 
            t = e.time

            if e.type == Event.ELEVATORSTOPS:
                elevator_i = elevatorList[e.elevatorNr]
                elev_nr = e.elevatorNr
                f = elevator_i.floornumber
                if self.show_otherprints:
                    print("elevator number",elev_nr,"stops at floor",elevator_i.floornumber, "at time",t, "with", len(queueElevator[elev_nr]),"people in it and direction upwards is", elevator_i.directionUp)

                if self.show_queues:
                    print("   queue at floor",f, "is length", len(queueFloor[f]))
                    if self.show_addremove:
                        for i in range(len(queueFloor[f])):
                            print("     Queued at floor",queueFloor[f][i])
                    print("   queue in elevator",elev_nr, "is length", len(queueElevator[elev_nr]))
                    if self.show_addremove:
                        for i in range(len(queueElevator[elev_nr])):
                            print("     In elevator",queueElevator[elev_nr][i])
                        

                Simulation.impatience(self, queueFloor, f, t)

                if self.show_queues:
                    print("   queue at floor",f, "is length", len(queueFloor[f])) 

                if len(queueElevator[elev_nr]) > 0 or len(queueFloor[f]) > 0: 
                    removeCustomers = []
                    for customer_elevator in queueElevator[elev_nr]: 
                        if customer_elevator.destinationFloor == f: 
                            removeCustomers.append(customer_elevator)
                            if self.show_addremove:
                                print("     - removing", customer_elevator)
                    addCustomers = []
                    for customer_floor in queueFloor[f]:
                        if customer_floor.directionUp == elevator_i.directionUp:
                            addCustomers.append(customer_floor)
                            
                            
                    if len(removeCustomers) > 0 or len(addCustomers) > 0:
                        t += self.doorDist.rvs()
                        if self.show_otherprints:
                            print("elevator doors opened at time",t)
                        for k in removeCustomers:
                            queueElevator[elev_nr].remove(k)
                            t += 1     

                        if self.show_otherprints:
                            print(len(removeCustomers),"customers left elevator at time", t) 
                                
                        if len(queueElevator[elev_nr]) < elevator_i.MAXPEOPLE:
                            customersThatGotInTheElevator = 0
                            customerThatWantInTheElevator = len(addCustomers) 
                            while len(addCustomers) > 0 and len(queueElevator[elev_nr]) < elevator_i.MAXPEOPLE:
                                customersThatGotInTheElevator += 1
                                if self.show_addremove:
                                    print("     + adding", addCustomers[0])
                                queueElevator[elev_nr].append(addCustomers[0])
                                queueFloor[f].remove(addCustomers[0])
                                t += 1
                                res.sumWaitingTime += t - addCustomers[0].arrivalTime
                                addCustomers.remove(addCustomers[0])
                            res.noEnteryLimitOfTheElevator +=  customerThatWantInTheElevator - customersThatGotInTheElevator
                        if self.show_otherprints:
                            print(customersThatGotInTheElevator, "customers got in the elvator at time", t)
                        res.sumPeopleInTheElevator += len(queueElevator[elev_nr])                
                        t += self.doorDist.rvs()
                        if self.show_otherprints:
                            print("elevator doors closed at time",t)   
                  
                        if self.show_queues:
                            print("   queue at floor",f, "is lenght", len(queueFloor[f])) 
                            if self.show_addremove:
                                for i in range(len(queueFloor[f])):
                                    print("     Queued at floor",queueFloor[f][i])
                            print("   queue in elevator",elev_nr, "is lenght", len(queueElevator[elev_nr]))
                            if self.show_addremove:
                                for i in range(len(queueElevator[elev_nr])):
                                    print("     In elevator",queueElevator[elev_nr][i])
                    
                if self.show_otherprints:
                    print("elevator number",elev_nr,"leaves floor",elevator_i.floornumber, "at time",t, "with", len(queueElevator[elev_nr]),"people in it and direction upwards is", elevator_i.directionUp)
                Elevator.newFloor(elevator_i, elevator_i.floornumber) # change the floor of the elevator to the next one and if needed change direction
                nextFloor = Event(Event.ELEVATORSTOPS, t+Elevator.MOVETIME, elevator_i.floornumber, elev_nr)#, elev_nr)
                fes.add(nextFloor)
                
                
            if e.type == Event.ARRIVAL: # arrival of a customer
                des = random.choices(range(Elevator.FLOORS), weights = probFloor[e.floor], k = 1)[0] 
                c = Customer(t, des, e.floor)
                res.allPeople += 1
                queueFloor[e.floor].append(c)
                if self.show_otherprints:
                    print("arrival of",c)
                a = self.arrDist[e.floor].rvs() 
                nextCustomer = Event(Event.ARRIVAL, t+a, e.floor)
                fes.add(nextCustomer)  

        res.totalTime = t 
        if self.show_res:
            print(res) 

    def impatience(self, queueFloor, floor_i, t): 
        if self.question6:
            removeCust = []
            for customernr_i in range(len(queueFloor[floor_i])):
                customer_i = queueFloor[floor_i][customernr_i]
                waittime_i = t - customer_i.arrivalTime
                if customer_i.directionUp:
                    if waittime_i >= self.impatienceUp[customer_i.floordiff]:
                        removeCust.append(customer_i)
                else:
                    if waittime_i >= self.impatienceDown[customer_i.floordiff]:
                        removeCust.append(customer_i)                  
            
            if self.show_otherprints:
                print(len(removeCust), "impatient customers left the queue at floor", floor_i)
            
            while len(removeCust) > 0:
                if self.show_addremove:    
                    print("     - removing impatient", removeCust[0], "left queue at time", t)
                queueFloor[removeCust[0].startFloor].remove(removeCust[0])
                removeCust.remove(removeCust[0])                   

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

nrElevators = 3 # amount of elevators, vary this number

impatienceDown = [0, 10, 20, 40, 60] # seconds before customer takes stairs for amount of floors downstairs
impatienceUp = [0, 30, 60, 100, 150] # seconds before customer takes stairs for amount of floors upstairs

# sim = Simulation(arrDist, doorDist, nrElevators, probFloor)
# sim = Simulation(arrDistQ5, doorDist, nrElevators, probFloorQ5) # for question 5
sim = Simulation(arrDist, doorDist, nrElevators, probFloor ,impatienceDown, impatienceUp, question6=True) # for question 6



sim.simulate(1000)

