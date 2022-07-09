'''
This is the file that actually runs the simulation, by importing the scheduling algorithms as files.
'''
import sys
import random
import math
from process import Process

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

    p = Process(0,0.01, 4096, 19)
    #print("arrival: " + str(p.arrival))
    #print("number of bursts: " + str(p.totalBursts))

    '''
    processes = 25
    lst = []
    random.seed(3)
    for i in range(processes):
        lst.append( Process(i,0.01, 3000))

    for i in range(processes):
        print(lst[i].arrival)
    '''       
        
    
    

    



