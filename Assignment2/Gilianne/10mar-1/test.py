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




    
    
    
    
    
    
    
    
    
    
    