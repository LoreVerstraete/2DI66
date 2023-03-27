import heapq
from collections import deque

class FES :
    
    def __init__(self):
        self.events = []
        
    def add(self, event):
        heapq.heappush(self.events, event)
    
    # to find the next first event without removing it?
    def checkNext(self):
        return self.events[0]
        # return heapq.nsmallest(1, self.events)
        #return heapq.heap[0](self.events)
        
    def next(self):
        return heapq.heappop(self.events)
    
    def isEmpty(self):
        return len(self.events) == 0
        
    def __str__(self):
        s = ''
        sortedEvents = sorted(self.events)
        for e in sortedEvents :
            s += str(e) + '\n'
        return s

#print(FES())