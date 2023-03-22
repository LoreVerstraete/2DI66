from numpy import array, zeros, mean
import random 
import matplotlib.pyplot as plt



probFloor = array([[0.0, 0.1, 0.3, 0.4, 0.2],
                   [0.7, 0.0, 0.1, 0.1, 0.1],
                   [0.6, 0.2, 0.0, 0.1, 0.1],
                   [0.6, 0.2, 0.1, 0.0, 0.1],
                   [0.5, 0.2, 0.2, 0.1, 0.0]])

nrRuns = 100000000
#randomNumber = zeros(nrRuns)


randomNumber = random.choices(range(5), weights = probFloor[0], k = nrRuns)


print(sum(array(randomNumber)==0))
print(mean(array(randomNumber)==1))
print(mean(array(randomNumber)==2))
print(mean(array(randomNumber)==3))
print(mean(array(randomNumber)==4))