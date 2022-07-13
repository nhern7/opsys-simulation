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

def checkFinished(process_list, terminated_processes, current_time):
    if len(terminated_processes) == 0:
        return False
    
    for i in process_list:
        if i.numCPUBursts != 0:
            return False
    
    for i in range(len(terminated_processes)):
        if current_time <= terminated_processes[i][0]+1:
            return False

    return True

def getQueueFormatted(ready_queue_formatted, ):
    ret = ""
    for i in ready_queue_formatted:
        ret += " " + i.name
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
    IO_processes = [] #keep track of all the processes currently performing IO
    terminated_processes = [] #keep track of all the processes that have been terminated    
    running = []
    almost_running = []
    ready_queue_formatted = []
    process_list_copy = list(process_list)
    time = 0
    time_added = 0
    running_CPU_original = 0 #the original CPU burst time (without any runtime being elasped) of the currently running process

    while(not checkFinished(process_list_copy, terminated_processes, time)):
        if time == 102:
            print()
        if len(running) == 1: 
            #if we completed a CPU burst and we still have more to go through
            if running[0][-1].CPUlst[0] == 0 and running[0][-1].numCPUBursts > 1:
                running[0][-1].numCPUBursts -= 1
                running[0][-1].CPUlst.pop(0)

                '''
                - I/O stuff and readding to the ready queue, if necessary (DO THIS IN SIMULATION)
                - output -> "Process _ terminated [current ready queue]" if necessary (DO THIS IN SIMULATION)
                '''
                if running[0][-1].numCPUBursts == 1:
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q:{}]".format(time, running[0][-1].name, running[0][-1].tau, running[0][-1].numCPUBursts, getQueueFormatted(ready_queue_formatted)))
                else:
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q:{}]".format(time, running[0][-1].name, running[0][-1].tau, running[0][-1].numCPUBursts, getQueueFormatted(ready_queue_formatted)))
                old_tau = running[0][-1].tau
                running[0][-1].tau = math.ceil(process.CPUguess(running[0][-1].tau, running_CPU_original, alpha))
                print("time {}ms: Recalculated tau for process {}: old tau {}ms; new tau {}ms [Q:{}]".format(time, running[0][-1].name, old_tau, running[0][-1].tau, getQueueFormatted(ready_queue_formatted)))

                #process starts its I/O
                #note: if here, no processes can be added to RUNNING STATE until 1ms passes
                IO_actual_time = running[0][-1].IOlst[0]+time+2
                print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q:{}]".format(time, running[0][-1].name, IO_actual_time, getQueueFormatted(ready_queue_formatted)))
                IO_processes.append( (IO_actual_time, running[0][-1], time) )
                
                running.pop(0)

            #if we completed a CPU burst and this was our last one for this process
            elif running[0][-1].CPUlst[0] == 0 and running[0][-1].numCPUBursts == 1:
                terminated_processes.append( (time, running[0][2]) )
                running[0][-1].numCPUBursts -= 1
                running[0][-1].CPUlst.pop(0)                
                print("time {}ms: Process {} terminated [Q:{}]".format(time, running[0][-1].name, getQueueFormatted(ready_queue_formatted, False)))
                running.pop(0)

        #checking for new arrivals to account for
        for i in range(len(process_list_copy)):
            if time == process_list_copy[i].arrival:
                time_added = time
                ready_queue_formatted.append(process_list[i])
                heapq.heappush(ready_queue, (process_list[i].tau, time_added, process_list[i]) ) #so stuff in the queue is ordered by estimated CPU burst time 
                print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, getQueueFormatted(ready_queue_formatted)))
    
        #if its ok to start running a new process
        if len(running) == 0 and len(ready_queue) > 0:
            #note: if any processes started performing IO at this time, wait 1ms to start running any new processes
            if len(IO_processes) > 0:
                if time > IO_processes[0][-1]+1:
                    
                    almost_running.append( (time,heapq.nsmallest(1, ready_queue)))
                    
                    #note: 1ms to remove from the READY QUEUE and add to RUNNING STATE
                    if time > almost_running[0][0]+1:
                        almost_running.pop(0)

                        #note: 1ms after being added into ready queue before being pulled out to run
                        if time > heapq.nsmallest(1, ready_queue)[0][1]+1:
                            p = heapq.heappop(ready_queue) #make sure we're pulling from the "front"
                            ready_queue_formatted.remove(p[-1].name)                            
                            running.append( p ) 
                            running_CPU_original = math.ceil(p[-1].CPUlst[0])
                            print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, process_list_copy[i].CPUlst[0], getQueueFormatted(ready_queue_formatted)) )
            else:
                if len(process_list_copy[i].CPUlst) > 0:
                    #note: 1ms to remove from the READY QUEUE and add to RUNNING STATE
                    if time > heapq.nsmallest(1, ready_queue)[0][1]+1:
                        p = heapq.heappop(ready_queue) #make sure we're pulling from the "front"
                        ready_queue_formatted.remove(p[-1])                                                    
                        running.append( p ) 
                        running_CPU_original = math.ceil(p[-1].CPUlst[0])
                        print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, process_list_copy[i].CPUlst[0], getQueueFormatted(ready_queue_formatted)) )                
        
        #if any processes are done performing IO
        temp = []
        for i in range(len(IO_processes)):
            if IO_processes[i][0] == time:
                IO_processes[i][1].IOlst.pop(0)                
                heapq.heappush(ready_queue, (IO_processes[i][1].tau, process_list[i].name, time, IO_processes[i][1]) ) 
                ready_queue_formatted.append(IO_processes[i][1])                
                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q:{}]".format(time, IO_processes[i][-1].name, IO_processes[i][-1].tau, getQueueFormatted(ready_queue_formatted)))
            else:
                temp.append(IO_processes[i])
        IO_processes = list(temp)

        #regular decrement of the running process' current CPU burst
        if len(running) == 1:
            #update some process info
            running[0][-1].CPUlst[0] -= 1        

        time+=1

    print("time {}ms: Simulator ended for SRT [Q:{}]".format(time, getQueueFormatted(ready_queue_formatted)))

    ''' use this as the way of maintaining the ready queue from this point forward...
    for i in range(len(process_list)):

        if process_list[i].tau < running_process.remaining:
            print(preempt)
        else:
            heapq.heappush(ready_queue, (process_list[i].tau, process_list[i].name) ) #so stuff in the queue is ordered by estimated CPU burst time
    '''
