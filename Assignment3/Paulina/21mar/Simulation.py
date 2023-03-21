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

class Simulation:
    ''' Describes the simulation '''
    def __init__(self, arrDist0, doorDist, nrElevators): #, arrDist1, arrDist2, arrDist3, arrDist4, doorDist, nrElevators):
        self.arrDist0 = arrDist0
        self.doorDist = doorDist
        self.nrElevators = nrElevators


    def simulate(self, T):
        fes = FES()
        res = Results()
        queue = deque() # for the first floor 
        queueElevator = deque()
        S = 0 # queue length integrated  
        q = 0 # queue length 
        t = 0 # time at the beginning 
        a = self.arrDist0.rvs()  # samples number of the next arrival 
        firstEvent = Event(Event.ARRIVAL, a)  # schedual frist event 
        elevator = Elevator(1)
        fes.add(firstEvent) # adding first event to future events 
        i=0
        while t<T: 
            print("round", i)
            i +=1
            e = fes.next()  # taking first element of the fes list and deleting this event 
            t = e.time
            if e.type == Event.ARRIVAL: 
                c = Customer(t, 1 ,0)
                print(c)
                queue.append(c)
                doorDist = self.doorDist.rvs()
                t += doorDist # Elevator.movingDoors(doorDist) # opend door time 
                print("door",doorDist)
                if  elevator.numberOfPeople < elevator.maxPeople:
                    queue.remove(c)
                    queueElevator.append(c)
                    t += 1
                doorDist = self.doorDist.rvs()
                t += doorDist
                print("door", doorDist)
                a = self.arrDist0.rvs() 
                nextEvent = Event(Event.ARRIVAL, a+t)
                print(nextEvent)
                fes.add(nextEvent)
                nextEvent = Event(Event.ELEVATORSTOPS, t+ Elevator.moveTime)
                if Elevator.floor == 0: # checks if the direction of he elevator needs to change 
                    Elevator.directionUp = True
                if Elevator.floor == 4: 
                    Elevator.directionUp = False
                Elevator.floor = Elevator.newFloor(Elevator.floor, Elevator.directionUp)

                print(nextEvent)
            elif e.type == Event.ELEVATORSTOPS:
                print("Queue: ",queueElevator)
                if  elevator.numberOfPeople > 0 and c.destinationFloor == 1:
                    Elevator.floors += 1
                    queueElevator.remove(c)
                    #print(queueElevator)

            


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

sim.simulate(10)

"""         self.arrDist1 = arrDist1
        self.arrDist2 = arrDist2
        self.arrDist3 = arrDist3
        self.arrDist4 = arrDist4 
"""