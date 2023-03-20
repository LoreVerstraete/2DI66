class Customer :
    enteringTime = 1
    leavingTime = 1

    def __init__(self, arr):
        self.arrivalTime = arr
        self.enterTime = 0 #arriving time + waitingtime, timestamp it starts to enter
        self.leaveTime = 0 #arriving time + waitingtime + servicetime, timestamp it ends leaving

    # def __lt__(self, otherCustomer):
    #     return self.arrivalTime < otherCustomer.arrivalTime
        
    def __str__(self):
        return "Customer at " + str(self.arrivalTime)

c = Customer(10)
print(c)