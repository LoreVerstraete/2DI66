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
        # elevator = [Elevator(elev) for elev in range(self.nrElevators)] # creates elevator for amount of elevators
        # print("elevator:", elevator)
        queueFloor = [deque() for floor in range(Elevator.FLOORS)] # makes a queue for each floor
        queueElevator = [deque() for elev in range(self.nrElevators)]  # makes a queue for each elevator 
        # print("queueElevator", queueElevator)
        firstCustomerArrivalTime = 100000
        for floor in range(Elevator.FLOORS):
            firstArrivalTime = self.arrDist[floor].rvs()  # samples number of the next arrival 
            print("first arrival for floor", floor, "at time", firstArrivalTime)
            firstArrivalEvent = Event(Event.ARRIVAL, firstArrivalTime, floor)  # schedule first event 
            fes.add(firstArrivalEvent) # adding first event to future events 
            if firstCustomerArrivalTime > firstArrivalTime:
                firstCustomerArrivalTime = firstArrivalTime
        elevatorList = []
        for elevatorI in arange(self.nrElevators):
            elevatorEvent = Event(Event.ELEVATORSTOPS, firstCustomerArrivalTime, 0, elevatorI)
            fes.add(elevatorEvent)
            elevatorList.append(Elevator(firstCustomerArrivalTime, elevatorI, 0))
            print("elevator", elevatorList[elevatorI], "nr", elevatorI, " starts at floor 0 at time", firstCustomerArrivalTime)
        # firstElevatorEvent = Event(Event.ELEVATORSTOPS, firstCustomerArrivalTime,0,0)
        # secondElevatorEvent = Event(Event.ELEVATORSTOPS, firstCustomerArrivalTime,0,1)
        # thirdElevatorEvent = Event(Event.ELEVATORSTOPS, firstCustomerArrivalTime,0,2)
        # print("elevator starts at floor 0 at time", firstCustomerArrivalTime)
        # fes.add(firstElevatorEvent)
        # fes.add(secondElevatorEvent)
        # fes.add(thirdElevatorEvent)
    
        
        round=0
        t = 0
        while t<T: 
            print("  ")
            print("round", round)
            round += 1
            e = fes.next()  # taking first element of the fes list and deleting this event 
            t = e.time

            if e.type == Event.ELEVATORSTOPS:
                #check if there are multiple elevators at the same time
                # moreElevators = True
                # elevatorsAtOnce = [] # create a list with multiple elevators
                # elevatorsAtOnce.append(elevatorList[e.elevatorNr]) # add the first elevator that is stopping
                # while moreElevators == True:
                #     more = fes.checkNext() # select the next event without removing it from the FES
                #     print("more", more)
                #     # check if the next event is equal to the initial event 
                #     if more.time == t and more.type == Event.ELEVATORSTOPS and e.floor == more.floor:
                #         print("yes multiple elevators")
                #         newEvent = fes.next() # select and remove the next event from the FES
                #         elevatorsAtOnce.append(elevatorList[newEvent.elevatorNr]) #add the elevator to the list of elevators

                #     else: # if the next even is not an elevator stopping it will change to False and just one event is used
                #         moreElevators = False
                
                # # if there are multiple elevators at one floor at the same time:
                # if len(elevatorsAtOnce) > 1:
                #     f = e.floor # the floor for all elevators should be the same
                #     if len(queueFloor[f]) > 0 or (len(queueElevator[elev_i]) > 0 for elev_i in elevatorsAtOnce ):
                #         print("yes people in queue or elevator")
                    
                
                # # if there is just one elevator at the floor
                # else:
                    # if more.time == t and more.type == Event.ARRIVAL and e.floor == more.floor:
                    #     print("people arrive when elevator is at certain floor")
                
                #for elev_i in range(nrElevators):
                # elevator = Elevator(t, e.elevatorNr, e.floor)
                elevator = elevatorList[e.elevatorNr]
                print("elevator information", elevator)
                elev_i = e.elevatorNr
                # print("elevator nr", elev_i)
                # f = elevator[elev_i].floornumber
                f = elevator.floornumber
                # print("elevator number",elev_i,"stops at floor",elevator[elev_i].floornumber, "at time",t, "with direction upwards is", elevator[elev_i].directionUp)
                print("elevator number",elev_i,"stops at floor",elevator.floornumber, "at time",t, "with direction upwards is", elevator.directionUp)

                # print("queueFloor", queueFloor)
                # print("xxxxxxxxxxxxxxxxxxx", len(queueFloor[f]))
                if len(queueElevator[elev_i]) > 0 or len(queueFloor[f]) > 0: 
                    removeCustomers = []
                    for customer_elevator in queueElevator[elev_i]: 
                        if customer_elevator.destinationFloor == f: 
                            removeCustomers.append(customer_elevator)
                            
                    print("remove Customers", removeCustomers)
                    addCustomers = []
                    for customer_floor in queueFloor[f]:
                        # if customer_floor.directionUp == elevator[elev_i].directionUp:
                        if customer_floor.directionUp == elevator.directionUp:
                            addCustomers.append(customer_floor)
                            
                            
                    if len(removeCustomers) > 0 or len(addCustomers) > 0:
                        t += self.doorDist.rvs()
                        print("elevator doors opened at time",t)
                        for k in removeCustomers:
                            queueElevator[elev_i].remove(k)
                            t += 1     

                        print(len(removeCustomers),"customers left elevator at time", t)            
                        
                        if len(queueElevator[elev_i]) < elevator.MAXPEOPLE:#elevator[elev_i].MAXPEOPLE:
                            customersThatGotInTheElevator = 0
                            customerThatWantInTheElevator = len(addCustomers) 
                            while len(addCustomers) > 0 and len(queueElevator[elev_i]) < elevator.MAXPEOPLE:#elevator[elev_i].MAXPEOPLE:
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
                print("elevator leaves with", len(queueElevator[elev_i]), "customers inside the elevator at time t =", t)  
                # Elevator.newFloor(elevator[elev_i]) # change the floor of the elevator to the next one and if needed change direction
                Elevator.newFloor(elevator, elevator.floornumber) # change the floor of the elevator to the next one and if needed change direction
                print("new floor",  elevator.floornumber)
                nextFloor = Event(Event.ELEVATORSTOPS, t+Elevator.MOVETIME, elevator.floornumber, elev_i)#, elev_i)
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
        # restEvents = len(fes.events) 
        # for peopleWaitingOrInElevator in range(restEvents):
        #     print(peopleWaitingOrInElevator)
        #     e = fes.next()
        #     if e.type == Event.ELEVATORSTOPS:
        #         f = elevator[0].floornumber
        #         if len(queueElevator[0]) > 0 or len(queueFloor[f]) > 0:
        #             t += self.doorDist.rvs()
        #             removeCustomers = []
        #             for customer_i in queueElevator[0]:  # CHANGED: [0] to the number of the elevator. 
        #                 print("customer", customer_i)
        #                 if customer_i.destinationFloor == f: 
        #                     removeCustomers.append(customer_i)
        #                     print("the i^th customer: ", customer_i)
        #             for k in removeCustomers:
        #                 queueElevator[0].remove(k)
        #             t += 1     

        #             if len(queueElevator[0]) < elevator[0].MAXPEOPLE:
        #                 for a in arange(Elevator.FLOORS):
        #                     if a == f:
        #                         print("right floor", "a", a, "f", f)
        #                         print("len q", len(queueFloor[a]))
        #                         customersThatGotInTheElevator = 0
        #                         customerThatWantInTheElevator = len(queueFloor[a])
        #                         while len(queueFloor[a]) > 0 and len(queueElevator[0]) < elevator[0].MAXPEOPLE:
        #                             customersThatGotInTheElevator += 1
        #                             print("only if queue")
        #                             c = queueFloor[a][0]
        #                             queueElevator[0].append(c)
        #                             res.sumWaitingTime += t - c.arrivalTime
        #                             print("waitingtime: ", res.sumWaitingTime, t)
        #                             t += 1
        #                             queueFloor[a].remove(c)
        #                         print("hallo",len(queueFloor[a]), customersThatGotInTheElevator)
        #                         res.noEnteryLimitOfTheElevator +=  customerThatWantInTheElevator - customersThatGotInTheElevator
        #                         print(res.noEnteryLimitOfTheElevator)
        #             print(len(queueElevator[0]))
        #             res.sumPeopleInTheElevator += len(queueElevator[0])                
        #             t += self.doorDist.rvs()                            
        #         print("t end", t)  
        #         if elevator[0].floornumber == 1:
        #             elevator[0].floornumber -= 1
        #         else: 
        #             elevator[0].floornumber += 1
        #         nextFloor = Event(Event.ELEVATORSTOPS, t+Elevator.MOVETIME)
        #         fes.add(nextFloor)
        # res.totalTime = t 
        # # print(res)                       

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

nrElevators = 3 # amount of elevators

sim = Simulation(arrDist, doorDist, nrElevators)

sim.simulate(200)
