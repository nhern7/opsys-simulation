'''
This is the file that actually runs the simulation, by importing the scheduling algorithms as files.
'''
import sys
import random
import math
import srt
from process import Process, Rand48
from FCFS import FCFS, FCFSwrite
import sjf 
import copy
from RR import RR

if __name__ == "__main__":
    
    if len(sys.argv) != 8:  #must be given exactly 8 args, else theres a problem...
        print("ERROR: improper arguments provided")
    else:
        n = int(sys.argv[1])     #number of processes
        seed = int(sys.argv[2])  #seed for pseudo-random number generation
        lamb = float(sys.argv[3])  #represents time between arrivals
        upper_bound = int(sys.argv[4])   #highest pseudo-random number allowed    
        t_cs = int(sys.argv[5])  #time it takes for a context switch
        alpha = float(sys.argv[6])     #represents alpha used during exponential averaging 
        t_slice = int(sys.argv[7])   #timeslice used in RR
        
        1 19 0.01 4096 4 0.5 64
        2 19 0.01 4096 4 0.5 64
        8 19 0.01 4096 4 0.75 32
        8 101 0.001 16384 4 0.5 128
        
        RNG = Rand48()
        RNG.srand(seed)
        process_list = []
        for i in range(n):
            temp = Process(i, lamb, upper_bound, RNG)
            process_list.append(temp)
        
        process_list_temp = []
        for i in range(n):
            process_list_temp.append(copy.deepcopy(process_list[i]) )  
                    
        for i in process_list:
            print("Process {}: arrival time {}ms; tau {}ms; {} CPU bursts:".format(i.name, i.arrival, i.tau, i.numCPUBursts))
            for j in range(i.numCPUBursts):
                if (j==i.numCPUBursts-1):
                    print("--> CPU burst {}ms".format(i.CPUlst[j]))
                else:
                    print("--> CPU burst {}ms --> I/O burst {}ms".format(i.CPUlst[j], i.IOlst[j]))
        print("")
        lst = FCFS(process_list, t_cs)  
        FCFSwrite("simout.txt",lst)   
        print()
        sjf.sjf(process_list_temp, alpha, "simout.txt")
        print()
        srt.algorithm(process_list, alpha, t_cs)
        srt.outputWriting("simout.txt")
        RNG = Rand48()
        RNG.srand(seed)
        process_list = []
        for i in range(n):
            temp = Process(i, lamb, upper_bound, RNG)
            process_list.append(temp)
        
        process_list_temp = []
        for i in range(n):
            process_list_temp.append(copy.deepcopy(process_list[i]) )  
                    
        print()
        RR(process_list_temp,t_cs,t_slice)
        
