'''
parts to do:

1. algorithm
2. measurements
3. output

SRT notes:
- basically sjf but with preemption

- processes are stored in the ready queue in order of smallest (shortest) predicted CPU burst time
to largest (longest)

- we need to know arrival times in order to preempt

- at least 1 unit of time must pass before considering preempting the current process

- upon entering ready queue, check if a process has a predicted CPU burst time < the remaining
predicted time of the currently running process. if so, a preemption occurs

- when a preemption occurs, the currently running process is added back to the ready queue.
'''

import heapq
import process
import math 

def checkFinished(process_list):
    for i in process_list:
        if len(i.CPUlst) != 0 or len(i.IOlst) != 0:
            return False
    return True

def getQueueFormatted(ready_queue):
    ret = ""
    for i in ready_queue:
        ret += " " + i[1]
    if ret == "":
        ret = " empty"
    return ret

def algorithm(process_list, alpha):
    '''
    have to use *predicted values* for sorting, 
    as they don't know how long a CPU burst will actually be. 

    this predicted value is the ending time, which is start time + tau

    remember ties are settled by alphaetical order

    everytime something is pushed to the queue, we should first check if it has a predicted
    CPU burst time that is < the remaining CPU burst time of the process curretly running
    '''
    print("time 0ms: Simulator started for SRT [Q: empty]")
    ready_queue = []
    running = []
    process_list_copy = list(process_list)
    time = 0
    time_added = 0
    running_CPU_original = 0 #the original CPU burst time (without any runtime being elasped) of the currently running process

    while(not checkFinished(process_list_copy)):
        if len(running) == 1: 
            if running[0][2].CPUlst[0] == 0: #means we finished a CPU burst
                #update some more process info
                running[0][2].numCPUBursts -= 1
                running[0][2].CPUlst = running[0][2].CPUlst[1:]

                '''
                - I/O stuff and readding to the ready queue, if necessary (DO THIS IN SIMULATION)
                - output -> "Process _ terminated [current ready queue]" if necessary (DO THIS IN SIMULATION)
                '''
                print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q:{}]".format(time, running[0][2].name, running[0][2].tau, running[0][2].numCPUBursts, getQueueFormatted(ready_queue)))
                old_tau = running[0][2].tau
                running[0][2].tau = math.ceil(process.CPUguess(running[0][2].tau, running_CPU_original, alpha))
                print("time {}ms: Recalculated tau for process {}: old tau {}ms; new tau {}ms [Q:{}]".format(time, running[0][2].name, old_tau, running[0][2].tau, getQueueFormatted(ready_queue)))
                running.pop(0)

        for i in range(len(process_list_copy)):
            if time == process_list_copy[i].arrival:
                time_added = time
                heapq.heappush(ready_queue, (process_list[i].tau, process_list[i].name, process_list[i]) ) #so stuff in the queue is ordered by estimated CPU burst time
                print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, getQueueFormatted(ready_queue)))

        if len(running) == 0 and len(ready_queue) > 0:
            #note, processes must wait 1 ms after being added into ready queue before being pulled out to run
            if time > time_added+1:
                p = heapq.heappop(ready_queue) #make sure we're pulling from the "front"
                running.append( p ) 
                running_CPU_original = math.ceil(p[2].CPUlst[0])
                print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, process_list_copy[i].CPUlst[0], getQueueFormatted(ready_queue)) )
        
        '''
        for i in range(len(process_list)):
            heapq.heappush(ready_queue, (process_list[i].tau, process_list[i].name) ) #so stuff in the queue is ordered by estimated CPU burst time
        '''

        if len(running) == 1:
            #update some process info
            running[0][2].CPUlst[0] -= 1

        time+=1
    print(list(ready_queue))


    
    ''' use this as the way of maintaining the ready queue from this point forward...
    for i in range(len(process_list)):

        if process_list[i].tau < running_process.remaining:
            print(preempt)
        else:
            heapq.heappush(ready_queue, (process_list[i].tau, process_list[i].name) ) #so stuff in the queue is ordered by estimated CPU burst time
    '''
if __name__ == "__main__":
    print()