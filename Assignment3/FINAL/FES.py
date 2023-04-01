import heapq

class FES :
    ''' Describes the future events set (FES)'''
    
    def __init__(self):
        ''' Initialise the FES '''
        self.events = []
        
    def add(self, event):
        ''' Add an event to FES '''
        heapq.heappush(self.events, event)
    
    def checkNext(self):
        ''' Returns the next event '''
        return self.events[0]
        
    def next(self):
        ''' Removes the next event out of the FES and returns this event '''
        return heapq.heappop(self.events)
        
    def __str__(self):
        ''' Returns a string of all events in the FES '''
        s = ''
        sortedEvents = sorted(self.events)
        for e in sortedEvents :
            s += str(e) + '\n'
        return s
