import random
import math

class Rand48(object):
    def __init__(self, seed):
        self.n = seed
    def seed(self, seed):
        self.n = seed
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    def drand(self):
        return self.next() / 2**48
    def lrand(self):
        return self.next() >> 17
    def mrand(self):
        n = self.next() >> 16
        if n & (1 << 31):
            n -= 1 << 32
        return n   



def next_exp(number_gen, lambdaNumb,upperBound):
        r = number_gen.drand()
        x = -math.log(r)/lambdaNumb
        while(1):
            if(x > upperBound):
                x = -math.log(r)/lambdaNumb
            else: 
                return x

class Process:
    
    def __init__(self, PrID, lambdaNumb, upperBound, seed):
        self.PrID = PrID #process ID number
        if(PrID < 26):
            self.name = chr(PrID+65) #Process number ID ASCII equivalent character
        else:
            print("invalid process ID") #if process ID number is larger than 25, it is invalid
        
        RNG = Rand48(seed)
        RNG.srand(seed)
        
        for i in range(500):
            print(next_exp(RNG, 0.01, 4096))
        '''
        self.arrival =  math.floor(next_exp(RNG, lambdaNumb, upperBound )) #initialize arrival time
        
        

        self.totalBursts = math.ceil(RNG.drand())*100 #calculate total burst time uniform distribution
        self.CPUBurstTime = math.ceil(next_exp(RNG, lambdaNumb, upperBound)) #calculate CPU burst time with exponential distribution
        self.IOBurstTime = math.ceil(next_exp(RNG, lambdaNumb, upperBound)) * 10 #calculate IO burst time with expoenential distribution
        '''



    


