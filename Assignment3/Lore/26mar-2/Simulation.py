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
    def __init__(self, arrDist, doorDist, nrElevators, probFloor):
        self.arrDist = arrDist
        self.doorDist = doorDist
        self.nrElevators = nrElevators
        self.probFloor = probFloor 


    def simulate(self, T):

        impatience_down = [0, 10, 20, 40, 60] # seconds before customer takes stairs for amount of floors downstairs
        impatience_up = [0, 30, 60, 100, 150] # seconds before customer takes stairs for amount of floors upstairs

        show_queues = False
        show_addremove = False
        show_otherprints = True
        show_res = False

        question_6 = True

        # initialize simulation
        fes = FES()
        res = Results()
        queueFloor = [deque() for floor in range(Elevator.FLOORS)] # makes a queue for each floor
        queueElevator = [deque() for elev in range(self.nrElevators)]  # makes a queue for each elevator 
        firstCustomerArrivalTime = T
        for floor in range(Elevator.FLOORS):
            firstArrivalTime = self.arrDist[floor].rvs()  # samples number of the next arrival 
            if show_otherprints:
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
            if show_otherprints:
                print("elevator nr", elevator_i, "starts at floor 0 at time", firstCustomerArrivalTime)
        
        round=0
        t = 0
        #while t<T: 
        while fes.checkNext().time <= T:
            if show_otherprints:
                print("  ")
                print("round", round)
                round += 1
            e = fes.next()  # taking first element of the fes list and deleting this event 
            t = e.time
            print("event str",e)

            if e.type == Event.ELEVATORSTOPS:
                elevator_i = elevatorList[e.elevatorNr]
                elev_nr = e.elevatorNr
                f = elevator_i.floornumber
                if show_otherprints:
                    print("elevator number",elev_nr,"stops at floor",elevator_i.floornumber, "at time",t, "with", len(queueElevator[elev_nr]),"people in it and direction upwards is", elevator_i.directionUp)

                if show_queues:
                    print("   queue at floor",f, "is lenght", len(queueFloor[f])) 
                    for i in range(len(queueFloor[f])):
                        print("     Queued at floor",queueFloor[f][i])
                    print("   queue in elevator",elev_nr, "is lenght", len(queueElevator[elev_nr]))
                    for i in range(len(queueElevator[elev_nr])):
                        print("     In elevator",queueElevator[elev_nr][i])
                    

                if len(queueElevator[elev_nr]) > 0 or len(queueFloor[f]) > 0: 
                    removeCustomers = []
                    for customer_elevator in queueElevator[elev_nr]: 
                        if customer_elevator.destinationFloor == f: 
                            removeCustomers.append(customer_elevator)
                            if show_addremove:
                                print("     - removing", customer_elevator)
                    addCustomers = []
                    for customer_floor in queueFloor[f]:
                        if customer_floor.directionUp == elevator_i.directionUp:
                            addCustomers.append(customer_floor)
                            
                            
                    if len(removeCustomers) > 0 or len(addCustomers) > 0:
                        t += self.doorDist.rvs()
                        if show_otherprints:
                            print("elevator doors opened at time",t)
                        for k in removeCustomers:
                            queueElevator[elev_nr].remove(k)
                            t += 1     

                        if show_otherprints:
                            print(len(removeCustomers),"customers left elevator at time", t) 
                                
                        if len(queueElevator[elev_nr]) < elevator_i.MAXPEOPLE:
                            customersThatGotInTheElevator = 0
                            customerThatWantInTheElevator = len(addCustomers) 
                            while len(addCustomers) > 0 and len(queueElevator[elev_nr]) < elevator_i.MAXPEOPLE:
                                customersThatGotInTheElevator += 1
                                if show_addremove:
                                    print("     + adding", addCustomers[0])
                                queueElevator[elev_nr].append(addCustomers[0])
                                queueFloor[f].remove(addCustomers[0])
                                t += 1
                                res.sumWaitingTime += t - addCustomers[0].arrivalTime
                                addCustomers.remove(addCustomers[0])
                            res.noEnteryLimitOfTheElevator +=  customerThatWantInTheElevator - customersThatGotInTheElevator
                        if show_otherprints:
                            print(customersThatGotInTheElevator, "customers got in the elvator at time", t)
                        res.sumPeopleInTheElevator += len(queueElevator[elev_nr])                
                        t += self.doorDist.rvs()
                        if show_otherprints:
                            print("elevator doors closed at time",t)   
                  
                        if show_queues:
                            print("   queue at floor",f, "is lenght", len(queueFloor[f])) 
                            for i in range(len(queueFloor[f])):
                                print("     Queued at floor",queueFloor[f][i])
                            print("   queue in elevator",elev_nr, "is lenght", len(queueElevator[elev_nr]))
                            for i in range(len(queueElevator[elev_nr])):
                                print("     In elevator",queueElevator[elev_nr][i])
                    
                if show_otherprints:
                    print("elevator number",elev_nr,"leaves floor",elevator_i.floornumber, "at time",t, "with", len(queueElevator[elev_nr]),"people in it and direction upwards is", elevator_i.directionUp)
                Elevator.newFloor(elevator_i, elevator_i.floornumber) # change the floor of the elevator to the next one and if needed change direction
                nextFloor = Event(Event.ELEVATORSTOPS, t+Elevator.MOVETIME, elevator_i.floornumber, elev_nr)#, elev_nr)
                fes.add(nextFloor)
                
                
            if e.type == Event.ARRIVAL: # arrival of a customer
                des = random.choices(range(Elevator.FLOORS), weights = probFloor[e.floor], k = 1)[0] 
                c = Customer(t, des, e.floor)
                res.allPeople += 1
                queueFloor[e.floor].append(c)
                if show_otherprints:
                    print(c)
                a = self.arrDist[e.floor].rvs() 
                nextCustomer = Event(Event.ARRIVAL, t+a, e.floor)
                fes.add(nextCustomer)   
        
            if question_6:
                removeCust = []
                for floor_i in range(Elevator.FLOORS):
                    for customernr_i in range(len(queueFloor[floor_i])):
                        customer_i = queueFloor[floor_i][customernr_i]
                        waittime_i = t - customer_i.arrivalTime
                        if customer_i.directionUp:
                            if waittime_i >= impatience_up[customer_i.floordiff]:
                                removeCust.append(customer_i)
                                print("impCust1", t, customer_i)
                        else:
                            if waittime_i >= impatience_up[customer_i.floordiff]:
                                removeCust.append(customer_i)
                                print("impCust1", t, customer_i)                        
                while len(removeCust) > 0:
                    impatientEvent = Event(Event.IMPATIENT, t, customer=removeCust[0])
                    fes.add(impatientEvent)
                    print("impCust2", t, removeCust[0])
                    queueFloor[removeCust[0].startFloor].remove(removeCust[0])
                    removeCust.remove(removeCust[0])

                if e.type == Event.IMPATIENT: # impatient customer takes the stairs
                    # print("queue at floor", e.customer.startFloor, "is length", len(queueFloor[e.customer.startFloor]))
                    # for customer_i in queueFloor[e.customer.startFloor]:
                    #     print("     Queued customer", customer_i)
                    print("impatient", e.customer, "removed at time",t)
                    # queueFloor[e.customer.startFloor].remove(e.customer)
                    # print("queue at floor", e.customer.startFloor, "is length", len(queueFloor[e.customer.startFloor]))
                    # for customer_i in queueFloor[e.customer.startFloor]:
                    #     print("     Queued customer", customer_i)
                    print("impCust3", t, e.customer)

        res.totalTime = t 
        if show_res:
            print(res)                       

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

sim = Simulation(arrDist, doorDist, nrElevators, probFloor)
# sim = Simulation(arrDistQ5, doorDist, nrElevators, probFloorQ5) # for question 5

impatience_down = [0, 10, 20, 40, 60] # seconds before customer takes stairs for amount of floors downstairs
impatience_up = [0, 30, 60, 100, 150] # seconds before customer takes stairs for amount of floors upstairs

sim.simulate(1000)

