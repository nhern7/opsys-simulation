import random
import math

class Rand48(object):
    def __init__(self):
        self.n = 0
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def drand(self):
        return self.next() / 2**48

def next_exp(number_gen, lambdaNumb,upperBound):
        r = number_gen.drand() #number gen is Rand48 object for 48 bit linear generator
        x = -math.log(r)/lambdaNumb #exponential distribution
        while(1):
            if(x > upperBound):
                x = -math.log(r)/lambdaNumb
            else: 
                return x

class Process:
    
    def __init__(self, PrID, lambdaNumb, upperBound, RNG):
        self.PrID = PrID #process ID number
        if(PrID < 26):
            self.name = chr(PrID+65) #Process number ID ASCII equivalent character
        else:
            print("invalid process ID") #if process ID number is larger than 25, it is invalid  
        
        self.arrival =  math.floor(next_exp(RNG,lambdaNumb, upperBound, )) #initialize arrival time
        self.totalBurst = math.ceil(RNG.drand()*100) #calculate total burst time uniform distribution
        self.tracker = 0
        self.CPUlst = []
        self.IOlst = []
        for i in range(self.totalBurst):
            self.CPUlst.append(math.ceil(next_exp(RNG,lambdaNumb, upperBound))) #calculate CPU burst time with exponential distribution
            self.IOlst.append(math.ceil(next_exp(RNG,lambdaNumb, upperBound)) * 10 )#calculate IO burst time with expoenential distribution
        self.IOlst.pop() #take out the last number from the IOlst



    


