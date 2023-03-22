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

    FLOORS = 5

    def __init__(self, arrDist, doorDist, nrElevators, probFloor): #, arrDist1, arrDist2, arrDist3, arrDist4, doorDist, nrElevators):
        self.arrDist = arrDist
        self.doorDist = doorDist
        self.nrElevators = nrElevators
        self.probFloor = probFloor 


    def simulate(self, Tend):
        # classes to create results and future events: 
        fes = FES()
        res = Results()

        # initzialising the objects:
        elevator = [Elevator(elev) for elev in range(self.nrElevators)] # creates elevator for amount of elevators

        queueFloor = [deque() for floor in range(self.FLOORS)] # makes a queue for each floor

        queueElevator = [deque() for elev in range(self.nrElevators)]  # makes a queue for each elevator 
        
        # Variables to kept track of the process during the simulation: 
        # S = 0 # queue length integrated  
        # q = 0 # queue length 
        t = 0 # time at the beginning 


        """ First create all customers (all c.) up to the last arrival is just after Tend for each floor 
        Then sort these customers by arrivaltime (does not matter which floor)
        Set t to the first arrival, then add this arrival to the system and remove this arrival from the FES
        When the first customer arrived (does not matter which floor), begin to move the elevator and check each of the floors
            
        While t < Tend:
            for all elevators:
                if elevator.floor == BOTTOMFLOOR
                    change elevator direction to going up
                if elevator.floor == TOPFLOOR
                    change elevator direction to going down

            for each floor:
                update the queue (check if another arrival appeared when passing each floor)
                if queueFloor = empty AND queueElevator == empty
                    pass
                if queueFloor != empty OR queueElevator != empty
                    if queueFloor has one or more persons who go in the same direction OR queueElevator has persons who want to get out at that floor
                        stop the elevator
                        open the doors
                        let people leave the elevator if needed
                        let people enter the elevator if needed
                        update the queue (maybe someone arrives again while opening/leaving/entering)
                        if people are added to the queue and want to go in the same direction
                            let them enter
                            update queue again (repeat this loop untill no others enter the queue at this floor)
                        close the doors
                go to the next floor
                
                this loop will be repeated the whole time (at least if there is one elevator)"""

        # creating the first users for each floor:
        # &&&&& COMMENT LORE: this should be done differently. 
        # &&&&& All user arrivaltimes should be calculated first and then added to the queue at a given time
        for i in range(self.FLOORS):
            c = Customer(self.arrDist[i].rvs(), random.choices(range(self.FLOORS), weights = probFloor[i], k = 1)[0], i)
            #  random.choices(range(5), weights = probFloor[0], k = nrRuns)
            queueFloor[i].append(c)
            print("startFloor:", c.startFloor, "endFloor:", c.destinationFloor, "arrivalTime:", c.arrivalTime )
            firstEvent = Event(Event.ARRIVAL, c.arrivalTime, c.startFloor, c.destinationFloor, c.directionUp)
            fes.add(firstEvent)

        print("queue floors:",queueFloor)
        print("queue elev:",queueElevator)
        # &&&&& COMMENT LORE: fes.next() function is wrongly used
        # &&&&& this should only be used when the stopped elevator lets people in (add NEXT from queueFloor to queueElevator, NEXT is first person in queue that wants to go in the same direction as the elevator)
        # &&&&& or when the stopped elevator lets people out (remove NEXT from queueu elevator, NEXT is first person in elevator that needs to leave the elevator at that floor)
        e = fes.next() 
        print("user: ", e.floor, e.destinationFloor, e.directionUp, e.arrtime )
        print("Goes elevator up?:",elevator[0].directionUp)

        # &&&&& COMMENT LORE: why append this event to the queue? why not just add the whole customer to the queue?
        queueFloor[e.floor].popleft()
        queueElevator[0].append(e.destinationFloor)
        print("queue floors:",queueFloor)
        print("queue elev:",queueElevator)
        while t < Tend: 
            # &&&&& COMMENT LORE: instead of checking where to go to, just move the elevator when queueFloor is empty. 
            # &&&&& The elevator can only move in one direction so where to go to does not matter, only if a queue is present
            # &&&&& then just move the elevator and check floor by floor if there are people on that specific floorqueue that want 
            # &&&&& to go the same direction as the elevator, then stop the elevator
            queueElevator[0].append(e.destinationFloor)
            if e.directionUp == elevator[0].directionUp:
                print(e.destinationFloor)
                elevator[0].floor = e.floor
                t += e.arrtime + e.floor * Elevator.MOVETIME # &&&&& COMMENT LORE: change this into the newfloor() function
            elif not (e.directionUp == elevator[0].directionUp):
                print("destination Floor: ",e.destinationFloor)
                print("current floor: ", e.floor)
                elevator[0].floor = e.floor
                t += e.arrtime + (e.floor + Elevator.FLOORS)* Elevator.MOVETIME # &&&&& COMMENT LORE: ? add arrival time to t?
                elevator[0].directionUp = not elevator[0].directionUp  # chnages direction of elevator 
            
            print("queue floors:",queueFloor)
            print("queue elev:",queueElevator)

            print("e.arrtime + e.floor * Elevator.MOVETIME",t)
            t = elevator[0].movingDoors(self.doorDist.rvs(),t)
            print("elevator ",t)
            t = elevator[0].newFloor(t)
            t = elevator[0].movingDoors(self.doorDist.rvs(),t)
            needTOMoveFloors = int(abs(e.destinationFloor-elevator[0].floor))
            print("needTOMoveFloors", needTOMoveFloors)
            for i in range(needTOMoveFloors):
                    t = elevator[0].movingDoors(self.doorDist.rvs(),t)
            print("elevator.MOVETIME * needTOMoveFloors",t)
            t = elevator[0].movingDoors(self.doorDist.rvs(),t)
            print("elevator.doorDist",t)
            queueElevator[0].pop()
            print(queueElevator[0])

        # while t < Tend: 
        #     queueElevatorOne.append(e.destinationFloor)
        #     if e.directionUp == elevator[0].directionUp:
        #         print(e.destinationFloor)
        #         elevator[0].floor = e.floor
        #         t += e.arrtime + e.floor * Elevator.MOVETIME
        #     elif not (e.directionUp == elevator[0].directionUp):
        #         print("destination Floor: ",e.destinationFloor)
        #         print("current floor: ", e.floor)
        #         elevator[0].floor = e.floor
        #         t += e.arrtime + (e.floor + Elevator.FLOORS)* Elevator.MOVETIME 
        #         elevator[0].directionUp = not elevator[0].directionUp  # chnages direction of elevator 
            
        #     print("e.arrtime + e.floor * Elevator.MOVETIME",t)
        #     elevator[0].movingDoors(self.doorDist.rvs())
        #     t += elevator[0].doorDist
        #     print("elevator ",t)
        #     elevator[0].newFloor()
        #     elevator[0].movingDoors(self.doorDist.rvs())
        #     needTOMoveFloors = int(abs(e.destinationFloor-elevator[0].floor))
        #     print("needTOMoveFloors", needTOMoveFloors)
        #     for i in range(needTOMoveFloors):
        #             elevator[0].movingDoors(self.doorDist.rvs())
        #     t += elevator[0].MOVETIME * needTOMoveFloors
        #     print("elevator.MOVETIME * needTOMoveFloors",t)
        #     elevator[0].movingDoors(self.doorDist.rvs())
        #     t += elevator[0].doorDist
        #     print("elevator.doorDist",t)
        #     queueElevatorOne.pop()
        #     print(queueElevatorOne)





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
