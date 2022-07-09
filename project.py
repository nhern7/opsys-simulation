'''
This is the file that actually runs the simulation, by importing the scheduling algorithms as files.
'''
import sys
import random
import numpy as np
import math
def next_exp(lambdaNumb,upperBound):
        r = random.uniform(0.0,1.0)
        x = -math.log(r)/lambdaNumb
        while(1):
            if(x > upperBound):
                x = -math.log(r)/lambdaNumb
            else: 
                return x



    

if __name__ == "__main__":
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
    

    


