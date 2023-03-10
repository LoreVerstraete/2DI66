queueInfo = [[21,4444],[11,43],[12,1]]


MinQueues = [i for i in range(len(queueInfo)) if len(queueInfo[i]) == min(len(queueInfo[j]) for j in range(len(queueInfo)))]
print(MinQueues)
# queue = random.choice(MinQueues) # if multiple queues are the shortest, pick random one
