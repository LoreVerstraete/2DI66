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

class simulation:
    ''' Describes the simulation '''
    def __init__(self, arrDist0, arrDist1, arrDist2, arrDist3, arrDist4, doorDist, nrElevators):
        self.arrDist0 = arrDist0
        self.arrDist1 = arrDist1
        self.arrDist2 = arrDist2
        self.arrDist3 = arrDist3
        self.arrDist4 = arrDist4
        self.doorDist = doorDist
        self.nrElevators = nrElevators

    def simulate(self, T):
        fes = FES()
        res = Results()
        queue = deque()
        S = 0 
        q = 0 
        t = 0 # time at the beginning 
        a = self.arrDist0.rvs()
        firstEvent = Event(Event.ARRIVAL, a)
        fes.add(firstEvent)
        res.registerQueueLength(t,len(queue))
        while t<T: 
            e = fes.next()
            tOld = t 
            customer = e.next()
            t = e.time()
            

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

elevators = 4 # amount of elevators

print(arrDist0.rvs())