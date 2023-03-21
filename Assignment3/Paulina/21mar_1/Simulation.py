from Customer import Customer
from Elevator import Elevator
from Distribution import Distribution
from scipy import stats
from collections import deque
from Results import Results
from numpy import *
from Event import Event 
from FES import FES 
import random 
import time

class Simulation:
    ''' Describes the simulation '''

    FLOORS = 4 

    def __init__(self, arrDist, doorDist, nrElevators, probFloor): #, arrDist1, arrDist2, arrDist3, arrDist4, doorDist, nrElevators):
        self.arrDist = arrDist
        self.doorDist = doorDist
        self.nrElevators = nrElevators
        self.probFloor = probFloor 


    def simulate(self, T):
        # classes to create results and future events: 
        fes = FES()
        res = Results()

        # initzialising the objects:
        elevator = Elevator(1)
        queueGroundFloor = deque() # for the first floor 
        queueFirstFloor = deque()
        queueSecondFloor = deque()
        queueThirdFloor = deque()
        queueFourthFloor = deque()
        queueAllFloors = deque()
        queueAllFloors.extend([queueGroundFloor, queueFirstFloor, queueSecondFloor, queueThirdFloor, queueFourthFloor])
        queueElevatorOne = deque()  # TODO: add the nested structure also fro the elevators 

        # Variables to kept track of the process during the simulation: 
        S = 0 # queue length integrated  
        q = 0 # queue length 
        t = 0 # time at the beginning 

        # creating the first unsers for each floor:  
        for i in range(self.FLOORS+1):
            c = Customer(self.arrDist[i].rvs(), random.choices(range(self.FLOORS + 1), weights = probFloor[i], k = 1)[0], 0)
            queueAllFloors[i].append(c)
            firstEvent = Event(Event.ARRIVAL, c.arrivalTime, c.startFloor, c.destinationFloor, c.directionUp)
            fes.add(firstEvent)
        
        i=0
        while t<T: 
            print("round", i)
            i +=1
            e = fes.next()  # taking first element of the fes list and deleting this event 
            cnew = Customer(self.arrDist[e.floor].rvs(), random.choices(range(Elevator.floors + 1), weights = probFloor[0], k = 1)[0], 0) #replacing customer
            queueAllFloors[e.floor].append(cnew)
            fes.add(Event(Event.ARRIVAL, cnew.arrivalTime, cnew.startFloor, cnew.destinationFloor, cnew.directionUp))
            t = e.time
            print(t)
            c1 = e.customer
            c1Floor = e.floor
            print("new Customer start floor: ",c1Floor)
            print("destination Floor: ", e.destinationFloor)
            if e.type == Event.ARRIVAL: 
                queueAllFloors[e.floor].append([e.time, e.destinationFloor])
                

                doorDist = self.doorDist.rvs()
                t += doorDist # Elevator.movingDoors(doorDist) # opend door time 
                print("door", doorDist)

"""                 if  elevator.numberOfPeople < elevator.maxPeople:
                    queueGroundFloor[0].remove(c1)
                    queueElevatorOne.append(c1)
                    t += 1
                doorDist = self.doorDist.rvs()
                t += doorDist
                print("door", doorDist)
                a = self.arrDist0.rvs() 
                nextEvent = Event(Event.ARRIVAL, a+t, 0)
                #print(nextEvent)
                fes.add(nextEvent)
                nextEvent = Event(Event.ELEVATORSTOPS, t+ Elevator.moveTime, 0)
                print("floor original: ", elevator.floor)
                if elevator.floor == 0: # checks if the direction of he elevator needs to change 
                    elevator.directionUp = True
                if elevator.floor == 1: 
                    elevator.directionUp = False
                elevator.floor = elevator.newFloor(elevator.floor, elevator.directionUp)
                print("floor new: ", elevator.floor)

                print(nextEvent)
            elif e.type == Event.ELEVATORSTOPS:
                print("Queue: ", queueElevatorOne)
                if  elevator.numberOfPeople > 0 and c.destinationFloor == 1:
                    Elevator.floors += 1
                    queueElevatorOne.remove(c) """


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

arrDist = [arrDist0, arrDist1, arrDist2, arrDist2, arrDist3, arrDist4]

doorDist = Distribution(stats.expon(scale = 3))

nrElevators = 1 # amount of elevators

#print(arrDist0.rvs())
sim = Simulation(arrDist, doorDist, nrElevators, probFloor)
#print(sim.simulate(3))


start = time.time()
sim.simulate(10)
end = time.time()

print("time: " , end-start)


"""         c0 = Customer(self.arrDist[0].rvs(), random.choices(range(Elevator.floors + 1), weights = probFloor[0], k = 1)[0], 0)
        c1 = Customer(self.arrDist[1].rvs(), random.choices(range(Elevator.floors + 1), weights = probFloor[1], k = 1)[0], 1)
        c2 = Customer(self.arrDist2.rvs(), random.choices(range(Elevator.floors + 1), weights = probFloor[2], k = 1)[0], 2)
        c3 = Customer(self.arrDist3.rvs(), random.choices(range(Elevator.floors + 1), weights = probFloor[3], k = 1)[0], 3)
        c4 = Customer(self.arrDist4.rvs(), random.choices(range(Elevator.floors + 1), weights = probFloor[4], k = 1)[0], 4)

        # appending each customer to there respective queue's:
        queueAllFloors[0].append(c0)
        queueAllFloors[1].append(c1)
        queueAllFloors[2].append(c2)
        queueAllFloors[3].append(c3)
        queueAllFloors[4].append(c4)


                # schedul the first events: 
        firstEvent0 = Event(Event.ARRIVAL, c0.arrivalTime, c0.startFloor, c0.destinationFloor, c0.directionUp)  # schedual frist event 
        firstEvent1 = Event(Event.ARRIVAL, c1.arrivalTime, c1.startFloor, c1.destinationFloor, c1.directionUp)
        firstEvent2 = Event(Event.ARRIVAL, c2.arrivalTime, c2.startFloor, c2.destinationFloor, c2.directionUp)
        firstEvent3 = Event(Event.ARRIVAL, c3.arrivalTime, c3.startFloor, c3.destinationFloor, c3.directionUp)
        firstEvent4 = Event(Event.ARRIVAL, c4.arrivalTime, c4.startFloor, c4.destinationFloor, c4.directionUp)

        #adding the arrival to the events: 
        fes.add(firstEvent0) # ground floor 
        fes.add(firstEvent1)
        fes.add(firstEvent2)
        fes.add(firstEvent3)
        fes.add(firstEvent4)
 """