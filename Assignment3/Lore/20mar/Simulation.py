# from Customer import Customer
# from Elevator import Elevator
from Distribution import Distribution
# from FCFSQueue import FCFSQueue
from scipy import stats
# from Results import Results
from numpy import *

class simulation:
    ''' Describes the simulation '''

probFloor = [[0, 0.1, 0.3, 0.4, 0.2],
             [0.7, 0, 0.1, 0.1, 0.1],
             [0.6, 0.2, 0, 0.1, 0.1],
             [0.6, 0.2, 0.1, 0, 0.1],
             [0.5, 0.2, 0.2, 0.1, 0]]

arrDist0 = Distribution(stats.expon(scale = 1/13.1))
arrDist1 = Distribution(stats.expon(scale = 1/3.4))
arrDist2 = Distribution(stats.expon(scale = 1/2.1))
arrDist3 = Distribution(stats.expon(scale = 1/9.2))
arrDist4 = Distribution(stats.expon(scale = 1/8.8))

doorDist = Distribution(stats.expon(scale = 3))

print(arrDist0.rvs())