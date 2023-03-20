class Customer :

    def __init__(self, arr):
        self.arrivalTime = arr
        
    def __lt__(self, otherCustomer):
        return self.arrivalTime < otherCustomer.arrivalTime
        
    def __str__(self):
        return "Customer at " + str(self.arrivalTime)