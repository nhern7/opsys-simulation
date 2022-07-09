import random
import math
def next_exp(lambdaNumb,upperBound):
        r = random.uniform(0.0,1.0)
        x = -math.log(r)/lambdaNumb
        while(1):
            if(x > upperBound):
                x = -math.log(r)/lambdaNumb
            else: 
                return x


class Process:
    
    def __init__(self, PrID, lambdaNumb, upperBound):
        self.PrID = PrID #process ID number
        if(PrID < 26):
            self.name = chr(PrID+65) #Process number ID ASCII equivalent character
        else:
            print("invalid process ID") #if process ID number is larger than 25, it is invalid
        self.arrival =  math.floor(next_exp(lambdaNumb, upperBound )) #initialize arrival time
        self.totalBurst = math.ceil(random.randrange(1,100)) #calculate total burst time uniform distribution

        self.CPUlst = []
        self.IOlst = []
        for i in range(self.totalBurst):
            self.CPUlst.append(math.ceil(next_exp(lambdaNumb, upperBound))) #calculate CPU burst time with exponential distribution
            self.IOlst.append(math.ceil(next_exp(lambdaNumb, upperBound)) * 10 )#calculate IO burst time with expoenential distribution




    


