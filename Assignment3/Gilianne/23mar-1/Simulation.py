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
    def __init__(self, arrDist0, doorDist, nrElevators): #, arrDist1, arrDist2, arrDist3, arrDist4, doorDist, nrElevators):
        self.arrDist0 = arrDist0
        self.doorDist = doorDist
        self.nrElevators = nrElevators


    def simulate(self, T):
        fes = FES()
        res = Results()
        queue = [deque() for i in arange(5)] # for the first floor 
        queueElevator = deque()
        S = 0 # queue length integrated  
        q = 0 # queue length 
        t = 0 # time at the beginning 
        a = self.arrDist0.rvs()  # samples number of the next arrival 
        print("first arrival", a)
        firstEvent = Event(Event.ARRIVAL, a, 0, 1)  # schedule first event 
        secondEvent = Event(Event.ELEVATORSTOPS, 0)
        elevator = Elevator(1)
        fes.add(firstEvent) # adding first event to future events 
        fes.add(secondEvent)
        i=0
        while t<T: 
            print("  ")
            print("round", i)
            i +=1
            e = fes.next()  # taking first element of the fes list and deleting this event 
            t = e.time
            print(e)
            if e.type == Event.ELEVATORSTOPS:
                f = elevator.floor
                print("floor: ",f)
                print('t start', t)
                
                if len(queueElevator) > 0 or len(queue[f]) > 0:
                # while len(queueElevator) > 0:
                    t += self.doorDist.rvs()
                    for i in queueElevator:
                        # i = queueElevator[0]
                        print("customer", i)
                        if i.destinationFloor == f:
                            queueElevator.remove(i)
                            t += 1                       
                    
                    if len(queueElevator) < elevator.maxPeople:
                        for a in arange(5):
                            if a == f:
                                print("right floor", "a", a, "f", f)
                                print("len q", len(queue[a]))
                                while len(queue[a]) > 0:
                                    print("only if queue")
                                    c = queue[a][0]
                                    queueElevator.append(c)
                                    t += 1
                                    queue[a].remove(c)
                                    
                    t += self.doorDist.rvs()                            
                print("t end", t)  
                if elevator.floor == 1:
                    elevator.floor -= 1
                else: 
                    elevator.floor += 1
                nextFloor = Event(Event.ELEVATORSTOPS, t+6)
                fes.add(nextFloor)
                
                
            if e.type == Event.ARRIVAL: # arrival of a customer
                for a in arange(5):
                    if e.floor == a:
                        des = random.randint(0,1)
                        print("des", des)
                        c = Customer(t, des, a)
                        queue[a].append(c)
                        print("queue", queue[a])
                        print(c)
                        a = self.arrDist0.rvs() 
                        nextCustomer = Event(Event.ARRIVAL, t+a)
                        fes.add(nextCustomer) 
            # if e.type == Event.ARRIVAL1:
            #     for a in arange(5):
            #         if e.floor == a:
            #             des = random.randint(0,1)
            #             print("des", des)
            #             c = Customer(t, des, a)
            #             queue[a].append(c)
            #             print("queue", queue[a])
            #             print(c)
            
                            
                    
            
            
            # if e.type == Event.ARRIVAL: 
            #     c = Customer(t, 1 ,0)
            #     print(c)
            #     queue.append(c)
            #     doorDist = self.doorDist.rvs()
            #     t += doorDist # Elevator.movingDoors(doorDist) # opend door time 
                
            #     print("door",doorDist)
            #     if  elevator.numberOfPeople < elevator.maxPeople:
            #         queue.remove(c)
            #         queueElevator.append(c)
            #         t += 1
            #     doorDist = self.doorDist.rvs()
            #     t += doorDist
            #     print("door", doorDist)
            #     a = self.arrDist0.rvs() 
            #     nextEvent = Event(Event.ARRIVAL, a+t)
            #     print(nextEvent)
            #     fes.add(nextEvent)
            #     nextEvent = Event(Event.ELEVATORSTOPS, t+ Elevator.moveTime)
            #     if elevator.floor == 0: # checks if the direction of he elevator needs to change 
            #         elevator.directionUp = True
            #     if elevator.floor == 4: 
            #         elevator.directionUp = False
            #     elevator.floor = elevator.newFloor(elevator.floor, elevator.directionUp)

            #     print(nextEvent)
            # elif e.type == Event.ELEVATORSTOPS:
            #     print("Queue: ",queueElevator)
            #     if  elevator.numberOfPeople > 0 and c.destinationFloor == 1:
            #         elevator.floors += 1
            #         queueElevator.remove(c)
            #         #print(queueElevator)

            


# destinationFloor = random.choices(range(nrStates), weights = p[x[i-1]], k = 1)[0] for x[i]
# choose floor: x[i] = random.choices(range(nrStates), weights = p[x[i-1]], k = 1)[0]


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

doorDist = Distribution(stats.expon(scale = 3))

nrElevators = 1 # amount of elevators

#print(arrDist0.rvs())
sim = Simulation(arrDist0, doorDist, nrElevators)
#print(sim.simulate(3))

sim.simulate(20)

"""         self.arrDist1 = arrDist1
        self.arrDist2 = arrDist2
        self.arrDist3 = arrDist3
        self.arrDist4 = arrDist4 
"""