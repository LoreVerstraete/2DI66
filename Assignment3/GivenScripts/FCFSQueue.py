'''
This class implements a standard queue in which customers are sorted on their arrival times.
Internally, we use a deque to represent the queue of customers. Basically, this is just a class
that has the exact same functionality as a deque (so one could argue that you can just as well 
use a deque instead).

@author: MBoon
'''
from collections import deque

from ch8.Customer import Customer


class FCFSQueue:
    
    def __init__(self):
        ''' 
        Creates an instance of a First-Come-First-Served (FCFS) queue.
        Initially, the queue contains no customers.
        '''
        self.customers = deque()  # internally we use a deque, which is the most efficient data structure for this purpose
        
    def add(self, customer):
        ''' 
        Adds a customer to (the back of) this queue.
        
        Parameters:
            customer: a customer object
        '''
        self.customers.append(customer)
        
    def insert(self, customer, index):
        ''' 
        Inserts a customer in this queue, at the specified position.
        Position 0 corresponds to the front of the queue.
        
        Parameters:
            customer: a customer object
            index: the index/position where to insert this customer
        '''
        self.customers.insert(index, customer)
        
    def removeFirst(self):
        ''' 
        Removes (and returns) the customer at the front of the queue.
        
        Returns:
            the customer object at position 0
        '''
        return self.customers.popleft()
    
    def remove(self, customer):
        ''' 
        Removes the specified customer from the queue.
        
        Parameters:
            customer: a customer object
        '''
        self.customers.remove(customer)
        
    def removeAt(self, index):
        ''' 
        Removes the customer at the specified index/position from the queue.
        Position 0 corresponds to the front of the queue.
        
        Parameters:
            index: the index/position where to remove a customer
        '''
        del self.customers[index]
        
    def position(self, customer):
        ''' 
        Returns the position of the specified customer in the queue.
        
        Returns:
            the index/position of the specified customer
        '''
        return self.customers.index(customer)
    
    def get(self, index):
        ''' 
        Returns the customer at the specified index in the queue.
        
        Returns:
            the customer object at the specified position 
        '''
        return self.customers[index]
        
    def size(self):
        ''' 
        Returns the number of customers in the queue (i.e., the queue length)
        
        Returns:
            the queue length
        '''
        return len(self.customers)
    
    def __str__(self):
        s = ''
        for c in self.customers:
            s += str(c) + '\n'
        return s
    
    
q = FCFSQueue()
for i in range(10):
    q.add(Customer(i))
print(q)
q.removeAt(3)
print(q)
q.add(Customer(5.5))
print(q)
