import heapq
from collections import deque

class FES :
    
    def __init__(self):
        self.events = []
        
    def add(self, event):
        heapq.heappush(self.events, event)
    
    def checkNext(self):
        return self.events[0]
        
    def next(self):
        return heapq.heappop(self.events)
        
    def __str__(self):
        s = ''
        sortedEvents = sorted(self.events)
        for e in sortedEvents :
            s += str(e) + '\n'
        return s

#print(FES())