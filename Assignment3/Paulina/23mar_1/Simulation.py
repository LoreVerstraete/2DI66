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

        a = self.arrDist[0].rvs()  # samples number of the next arrival 
        print("first arrival", a)
        firstEvent = Event(Event.ARRIVAL, a, 0)  # schedule first event 
        secondEvent = Event(Event.ELEVATORSTOPS, 0)
        elevator = Elevator(1)
        fes.add(firstEvent) # adding first event to future events 
        fes.add(secondEvent)
        round=0
        t = 0
        while t<T: 
            print("  ")
            print("round", round)
            round +=1
            e = fes.next()  # taking first element of the fes list and deleting this event 
            t = e.time
            print(e)
            if e.type == Event.ELEVATORSTOPS:
                f = elevator.floornumber
                print("floor: ",f)
                print('t start', t)
                
                if len(queueElevator) > 0 or len(queueFloor[f]) > 0:
                # while len(queueElevator) > 0:
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
                                   
                    
                    if len(queueElevator[0]) < elevator.MAXPEOPLE:
                        for a in arange(Elevator.FLOORS):
                            if a == f:
                                print("right floor", "a", a, "f", f)
                                print("len q", len(queueFloor[a]))
                                customersThatGotInTheElevator = 0
                                customerThatWantInTheElevator = len(queueFloor[a])
                                while len(queueFloor[a]) > 0 and len(queueElevator[0]) < elevator.MAXPEOPLE:
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
                if elevator.floornumber == 1:
                    elevator.floornumber -= 1
                else: 
                    elevator.floornumber += 1
                nextFloor = Event(Event.ELEVATORSTOPS, t+Elevator.MOVETIME)
                fes.add(nextFloor)
                
                
            if e.type == Event.ARRIVAL: # arrival of a customer
                for floor_i in arange(Elevator.FLOORS):
                    if e.floor == floor_i:
                        des = random.choices(range(Elevator.FLOORS), weights = probFloor[floor_i], k = 1)[0] 
                        print("des", des)
                        c = Customer(t, des, floor_i)
                        res.allPeople += 1
                        queueFloor[floor_i].append(c)
                       # print("queue", queueFloor[floor_i])
                        print(c)
                        a = self.arrDist[floor_i].rvs() 
                        nextCustomer = Event(Event.ARRIVAL, t+a, e.floor)
                        fes.add(nextCustomer)   
        res.totalTime = t 
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

nrElevators = 1 # amount of elevators

#print(arrDist0.rvs())
sim = Simulation(arrDist, doorDist, nrElevators)
#print(sim.simulate(3))

sim.simulate(20)
