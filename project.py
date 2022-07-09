'''
This is the file that actually runs the simulation, by importing the scheduling algorithms as files.
'''
import sys
import random
import math
from process import Process

'''
def next_exp(lambdaNumb,upperBound):
        r = random.uniform(0.0,1.0)
        x = -math.log(r)/lambdaNumb
        while(1):
            if(x > upperBound):
                x = -math.log(r)/lambdaNumb
            else: 
                return x
'''


if __name__ == "__main__":
    '''
    if len(sys.argv) != 8:  #must be given exactly 8 args, else theres a problem...
        print("we have problems")
    else:
        n = sys.argv[1]     #number of processes
        seed = sys.argv[2]  #seed for pseudo-random number generation
        lamb = sys.argv[3]  #represents time between arrivals
        upper_bound = sys.argv[4]   #highest pseudo-random number allowed    
        t_cs = sys.argv[5]  #time it takes for a context switch
        alpha = sys.argv[6]     #represents alpha used during exponential averaging 
        t_slice = sys.argv[1]   #timeslice used in RR
        '''

    processes = 3
    lst = []
    random.seed(3)
    for i in range(processes):
        lst.append( Process(i,0.01, 3000))

    for i in range(processes):
        print(lst[i].CPUlst)
        print("bruh")
           
        
    
    

    



