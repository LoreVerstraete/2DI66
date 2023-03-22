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
            c = Customer(self.arrDist[i].rvs(), random.choices(range(self.FLOORS + 1), weights = probFloor[i], k = 1)[0], i)

            #  random.choices(range(5), weights = probFloor[0], k = nrRuns)
            queueAllFloors[i].append(c)
            print("start", c.startFloor, "end", c.destinationFloor, "arrival time", c.arrivalTime )
            firstEvent = Event(Event.ARRIVAL, c.arrivalTime, c.startFloor, c.destinationFloor, c.directionUp)
            fes.add(firstEvent)


        e = fes.next()
        print("user: ",  e.floor, e.destinationFloor, e.directionUp, e.arrtime )
        print(elevator.directionUp)
        queueElevatorOne.append(e.destinationFloor)
        
        while t < T: 
            queueElevatorOne.append(e.destinationFloor)
            if e.directionUp == elevator.directionUp:
                print(e.destinationFloor)
                elevator.floor = e.floor
                t += e.arrtime + e.floor * Elevator.MOVETIME
            elif not (e.directionUp == elevator.directionUp):
                print("destination Floor: ",e.destinationFloor)
                print("current floor: ", e.floor)
                elevator.floor = e.floor
                t += e.arrtime + (e.floor + Elevator.FLOORS)* Elevator.MOVETIME 
                elevator.directionUp = not elevator.directionUp  # chnages direction of elevator 
            
            print("e.arrtime + e.floor * Elevator.MOVETIME",t)
            elevator.movingDoors(self.doorDist.rvs())
            t += elevator.doorDist
            print("elevator ",t)
            elevator.newFloor(elevator.floor, elevator.directionUp)
            elevator.movingDoors(self.doorDist.rvs())
            needTOMoveFloors = int(abs(e.destinationFloor-elevator.floor))
            print("needTOMoveFloors", needTOMoveFloors)
            for i in range(needTOMoveFloors):
                    elevator.movingDoors(self.doorDist.rvs())
            t += elevator.MOVETIME * needTOMoveFloors
            print("elevator.MOVETIME * needTOMoveFloors",t)
            elevator.movingDoors(self.doorDist.rvs())
            t += elevator.doorDist
            print("elevator.doorDist",t)
            queueElevatorOne.pop()
            print(queueElevatorOne)





probFloor = array([[0.0, 0.1, 0.3, 0.4, 0.2],
                   [0.7, 0.0, 0.1, 0.1, 0.1],
                   [0.6, 0.2, 0.0, 0.1, 0.1],
                   [0.6, 0.2, 0.1, 0.0, 0.1],
                   [0.5, 0.2, 0.2, 0.1, 0.0]])

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
sim.simulate(15)
end = time.time()

print("time: " , end-start)
