import pandas as pd

from numpy import mean 
# data = [(2, 1, 57, 5.033295127182561, 62.03329512718256, 'card', 0, 0, 12.719789203659083, 74.75308433084165)
# b = (0, [1, 57, 40.383531757963524, 97.38353175796352, 'card', 1, 0, 38.01582320607464, 135.39935496403817])
# c = (3, [1, 57, 44.62117432654122, 101.62117432654122, 'cash', 2, 0, 6.524635831349784, 108.145810157891])
# d = (4, [1, 57, 64.99062997981657, 121.99062997981657, 'card', 0, 0, 7.257719709882325, 129.2483496896989])
# e = (1, [1, 57, 87.69470681745901, 144.694706817459, 'card', 1, 0, 20.742239364355235, 165.43694618181425])
# f = (5, [2, 125, 54.871034132850525, 179.87103413285053, 'card', 0, 0, 0.04657808256904987, 179.91761221541958])
# g = (7, [3, 182, 35.89537809293199, 217.895378092932, 'cash', 2, 0, 37.62374980814699, 255.51912790107897])
# h = (6, [3, 182, 86.31398541887421, 268.3139854188742, 'cash', 0, 0, 40.83737215470144, 309.15135757357564])
# i = (8, [3, 182, 89.39774757922835, 271.39774757922834, 'cash', 1, 0, 26.587403438563552, 297.9851510177919])
# j = (9, [3, 182, 152.0240764815775, 334.0240764815775, 'card', 0, 0, 5.780611027498663, 339.80468750907613])

data = [(2, 1, 57, 5.033295127182561, 62.03329512718256, 'card', 0, 0, 12.719789203659083, 74.75308433084165), (0, 1, 57, 40.383531757963524, 97.38353175796352, 'card', 1, 0, 38.01582320607464, 135.39935496403817),
(3, 1, 57, 44.62117432654122, 101.62117432654122, 'cash', 2, 0, 6.524635831349784, 108.145810157891),
(4, 1, 57, 64.99062997981657, 121.99062997981657, 'card', 0, 0, 7.257719709882325, 129.2483496896989),
(1, 1, 57, 87.69470681745901, 144.694706817459, 'card', 1, 0, 20.742239364355235, 165.43694618181425),
(5, 2, 125, 54.871034132850525, 179.87103413285053, 'card', 0, 0, 0.04657808256904987, 179.91761221541958),
(7, 3, 182, 35.89537809293199, 217.895378092932, 'cash', 2, 0, 37.62374980814699, 255.51912790107897),
(6, 3, 182, 86.31398541887421, 268.3139854188742, 'cash', 0, 0, 40.83737215470144, 309.15135757357564), 
(8, 3, 182, 89.39774757922835, 271.39774757922834, 'cash', 1, 0, 26.587403438563552, 297.9851510177919),
(9, 3, 182, 152.0240764815775, 334.0240764815775, 'card', 0, 0, 5.780611027498663, 339.80468750907613)]

dataframe = pd.DataFrame(data, columns = ["customerNr", "GroupNr", "arrTime", "timeFood", "timeQueue", "cashCard", "nrQueue", "waitTime", "serviceTime", "finishTime"])
dataframe["sojourn"] = dataframe["finishTime"] - dataframe["arrTime"]
meanvalue = mean(dataframe["sojourn"])







#%%
queueInfo = [[21],[11,43],[12,1]]


MinQueues = [i for i in range(len(queueInfo)) if len(queueInfo[i]) == min(len(queueInfo[j]) for j in range(len(queueInfo)))]
print(MinQueues)
# queue = random.choice(MinQueues) # if multiple queues are the shortest, pick random one



#%%
#check extension 1
  
        servicetimelist0 = []
        servicetimelist1 = []
        servicetimelist2 = []
        for i in range(len(sim[1])):
            if sim[1][i][1][nrQueue] == 0:
                servicetimelist0.append(sim[1][i][1][serviceTime])
            if sim[1][i][1][nrQueue] == 1:
                servicetimelist1.append(sim[1][i][1][serviceTime])
            if sim[1][i][1][nrQueue] == 2:
                servicetimelist2.append(sim[1][i][1][serviceTime])
        print("mean service queue 0", mean(servicetimelist0))
        print("std service queue 1", std(servicetimelist0))
        print("mean service queue 0", mean(servicetimelist1))
        print("std service queue 1", std(servicetimelist1))    
        print("mean service queue 0", mean(servicetimelist2))
        print("std service queue 1", std(servicetimelist2)) 
        
#%%
meancash = 20
servicetime = random.exponential(meancash*1.25) 
print(servicetime)
servicetime = random.exponential(meancash)*1.25
print(servicetime)

servicetime1 = []
servicetime2 = []
for i in range(0, 1000):
    servicetime = random.exponential(meancash*1.25) 
    servicetime1.append(servicetime)
    servicetime = random.exponential(meancash)*1.25
    servicetime2.append(servicetime)

print(mean(servicetime1))
print(mean(servicetime2))


#%%

long = 10

randomnumbers = [random.uniform(0,10) for i in range(0, long)]
randomnumbers = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5,10.5]
print(randomnumbers)
randomnumbers = [round(randomnumbers[i],0) for i in range(0, len(randomnumbers))]
print("rounded", randomnumbers)




    
    
    
    
    
    
    
    
    
    
    