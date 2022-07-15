import heapq
import process
import math 
import copy

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

def getQueueFormatted(ready_queue_formatted):
    ret = ""
    for i in ready_queue_formatted:
        ret += " " + i.name
    if ret == "":
        ret = " empty"
    return ret

def algorithm(process_list, alpha, t_cs):
    print("time 0ms: Simulator started for SRT [Q: empty]")
    
    ready_queue = [] #
    IO_processes = [] #keep track of all the processes currently performing IO: time IO ends, process, time added
    terminated_processes = [] #keep track of all the processes that have been terminated    
    running = [] #keep track of the running process: tau, time added, process
    #almost_running = [] #keep track of the next process to start running
    ready_queue_formatted = [] #used for formatting only

    process_list_copy = [] #maintain all the process. make changes to them through this list only
    for i in process_list:
        process_list_copy.append(copy.deepcopy(i))

    time = 0 #sim time
    time_added = 0 #time a process is added to the ready queue
    running_CPU_original = 0 #the original CPU burst time (without any runtime being elasped) of the currently running process

    #stats set up below
    global total_context_switches
    total_context_switches = 0

    global utilization
    utilization = 0

    global total_preemptions
    total_preemptions = 0 

    global total_cs_time
    total_cs_time = 0

    total_CPU_burst_time = 0
    total_CPU_burst_count = 0
    total_turnaround_time = 0
    must_waits = 0
    LAST = 0

    while(not checkFinished(process_list_copy, terminated_processes, time)):

        if len(running) == 1: 
            #if we completed a CPU burst and we still have more to go through
            if running[0][-1].CPUlst[0] == 0 and running[0][-1].numCPUBursts > 1:
                running[0][-1].numCPUBursts -= 1
                running[0][-1].CPUlst.pop(0)
                if running[0][-1].numCPUBursts == 1:
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q:{}]".format(time, running[0][-1].name, running[0][-1].tau, running[0][-1].numCPUBursts, getQueueFormatted(ready_queue_formatted)))
                else:
                    print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q:{}]".format(time, running[0][-1].name, running[0][-1].tau, running[0][-1].numCPUBursts, getQueueFormatted(ready_queue_formatted)))
                
                old_tau = running[0][-1].tau
                running[0][-1].tau = math.ceil(process.CPUguess(running[0][-1].tau, running_CPU_original, alpha))
                print("time {}ms: Recalculated tau for process {}: old tau {}ms; new tau {}ms [Q:{}]".format(time, running[0][-1].name, old_tau, running[0][-1].tau, getQueueFormatted(ready_queue_formatted)))

                #process starts its I/O
                IO_actual_time = running[0][-1].IOlst[0]+time+(t_cs/2)
                print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q:{}]".format(time, running[0][-1].name, IO_actual_time, getQueueFormatted(ready_queue_formatted)))
                IO_processes.append( (IO_actual_time, running[0][-1], time) )
                LAST = time
                if len(ready_queue) > 0:
                    must_waits += 1

                #context_switch stuff
                total_cs_time += t_cs/2

                running.pop(0)

            #if we completed a CPU burst and this was our last one for this process
            elif running[0][-1].CPUlst[0] == 0 and running[0][-1].numCPUBursts == 1:
                terminated_processes.append( (time, running[0][2]) )
                running[0][-1].numCPUBursts -= 1
                running[0][-1].CPUlst.pop(0)      
                print("time {}ms: Process {} terminated [Q:{}]".format(time, running[0][-1].name, getQueueFormatted(ready_queue_formatted)))

                #context_switch stuff
                total_cs_time += t_cs/2

                running.pop(0)

        #checking for new arrivals to account for
        for i in range(len(process_list_copy)):
            if time == process_list_copy[i].arrival:
                time_added = time
                process_list_copy[i].burst_arrival = time
                
                #check if we should preempt or not
                if len(running) > 0:
                    if process_list_copy[i].tau < (time-running[0][-1].tau):
                        #preemption occurs here!!!!!!
                        
                        ready_queue_formatted.append(running[0][-1])
                        heapq.heappush(ready_queue, (running[0][-1].tau, time_added, running[0][-1]) )
                        print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(time, running[0][-1].name, running[0][-1].tau, getQueueFormatted(ready_queue_formatted))) 
                        LAST = time
                        running.pop(0)
                        
                        #do we have any more bursts to run?
                        if len(process_list_copy[i].CPUlst) > 0:
                            #has enough time passed to run? aka has a full context switch occured?
                            if time >= LAST+t_cs:
                                #reset and set up stuff
                                must_waits = 0
                                ready_queue_formatted.remove(process_list_copy[i])                                                    
                                running.append( p ) 
                                running_CPU_original = math.ceil(process_list_copy[i].CPUlst[0])

                                #stats stuff
                                total_cs_time += t_cs
                                total_CPU_burst_time += process_list_copy[i].CPUlst[0]
                                total_CPU_burst_count += 1
                                total_turnaround_time += ((time-p[1]) + total_CPU_burst_time + total_cs_time) #should be wait time + cpu burst time + context switch time accrued during this burst
                                utilization += (process_list_copy[i].CPUlst[0]/time)
                                process_list_copy[i].burst_wait_list.append(time - process_list_copy[i].burst_arrival)
                                total_context_switches += 1

                                print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, process_list_copy[i].CPUlst[0], getQueueFormatted(ready_queue_formatted)) )                                        
                    
                    else:    
                        ready_queue_formatted.append(process_list_copy[i])
                        heapq.heappush(ready_queue, (process_list_copy[i].tau, time_added, process_list_copy[i]) ) #so stuff in the queue is ordered by estimated CPU burst time 
                        print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, getQueueFormatted(ready_queue_formatted)))
                else:
                    ready_queue_formatted.append(process_list_copy[i])
                    heapq.heappush(ready_queue, (process_list_copy[i].tau, time_added, process_list_copy[i]) )
                    print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, getQueueFormatted(ready_queue_formatted)))                    
        time_added = 0

        #if its ok to start running a new process
        if len(running) == 0 and len(ready_queue) > 0:

            #only here if a process has just finished running prior to this
            if len(IO_processes) > 0:
                    
                #check if all the context switching time has been included
                if time >= LAST+((must_waits+1)*(t_cs/2)):
                    #reset and set up stuff
                    must_waits = 0
                    p = heapq.heappop(ready_queue) #make sure we're pulling from the "front"
                    ready_queue_formatted.remove(p[-1])                            
                    running.append( p ) 
                    running_CPU_original = math.ceil(p[-1].CPUlst[0])

                    #stats stuff
                    total_cs_time += t_cs
                    total_CPU_burst_time += process_list_copy[i].CPUlst[0]
                    total_CPU_burst_count += 1
                    total_turnaround_time += ((time-p[1]) + total_CPU_burst_time + total_cs_time) #should be wait time + cpu burst time + context switch time
                    utilization += (p[-1].CPUlst[0]/time)
                    p[-1].burst_wait_list.append(time - p[-1].burst_arrival)
                    total_context_switches += 1

                    print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, process_list_copy[i].CPUlst[0], getQueueFormatted(ready_queue_formatted)) )

            else:#only here if NO process has just finished running prior to this
                
                #do we have any more bursts to run?
                if len(process_list_copy[i].CPUlst) > 0:
                    
                    #has enough time passed to run? aka has the second half of context switch occured?
                    if time >= heapq.nsmallest(1, ready_queue)[0][1]+(t_cs/2):
                        #reset and set up stuff
                        must_waits = 0
                        p = heapq.heappop(ready_queue) #make sure we're pulling from the "front"
                        ready_queue_formatted.remove(p[-1])                                                    
                        running.append( p ) 
                        running_CPU_original = math.ceil(p[-1].CPUlst[0])

                        #stats stuff
                        total_cs_time += t_cs
                        total_CPU_burst_time += process_list_copy[i].CPUlst[0]
                        total_CPU_burst_count += 1
                        total_turnaround_time += ((time-p[1]) + total_CPU_burst_time + total_cs_time) #should be wait time + cpu burst time + context switch time
                        utilization += (p[-1].CPUlst[0]/time)
                        p[-1].burst_wait_list.append(time - p[-1].burst_arrival)
                        total_context_switches += 1

                        print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, process_list_copy[i].CPUlst[0], getQueueFormatted(ready_queue_formatted)) )                
        
        #if any processes are done performing IO
        temp = []
        for i in range(len(IO_processes)):
            if IO_processes[i][0] == time:
                
                #check if we should preempt or not
                if len(running) > 0:
                    if IO_processes[i][1].tau < (time-running[0][-1].tau):
                        
                        #preemption occurs here!!!!!!
                        
                        ready_queue_formatted.append(running[0][-1])
                        heapq.heappush(ready_queue, (running[0][-1].tau, time_added, running[0][-1]) )
                        print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(time, running[0][-1].name, running[0][-1].tau, getQueueFormatted(ready_queue_formatted))) 
                        LAST = time
                        running.pop(0)
                    
                        #do we have any more bursts to run?
                        if len(IO_processes[i][1].CPUlst) > 0:
                            #has enough time passed to run? aka has a full context switch occured?
                            if time >= LAST+t_cs:
                                #reset and set up stuff
                                must_waits = 0
                                ready_queue_formatted.remove(IO_processes[i][1])                                                    
                                running.append( p ) 
                                running_CPU_original = math.ceil(IO_processes[i][1].CPUlst[0])

                                #stats stuff
                                total_cs_time += t_cs
                                total_CPU_burst_time += IO_processes[i][1].CPUlst[0]
                                total_CPU_burst_count += 1
                                total_turnaround_time += ((time-p[1]) + total_CPU_burst_time + total_cs_time) #should be wait time + cpu burst time + context switch time accrued during this burst
                                utilization += (IO_processes[i][1].CPUlst[0]/time)
                                IO_processes[i][1].burst_wait_list.append(time - IO_processes[i][1].burst_arrival)
                                total_context_switches += 1

                                print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, IO_processes[i][1].name, IO_processes[i][1].tau, IO_processes[i][1].CPUlst[0], getQueueFormatted(ready_queue_formatted)) )                                        

                IO_processes[i][1].IOlst.pop(0)                
                heapq.heappush(ready_queue, (IO_processes[i][1].tau, time, IO_processes[i][1]) ) 
                ready_queue_formatted.append(IO_processes[i][1])   
                LAST = time           
                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q:{}]".format(time, IO_processes[i][1].name, IO_processes[i][1].tau, getQueueFormatted(ready_queue_formatted)))
            else:
                temp.append(IO_processes[i])
        IO_processes = list(temp)

        #regular decrement of the running process' current CPU burst
        if len(running) == 1:
            #update some process info
            running[0][-1].CPUlst[0] -= 1        

        time+=1

    print("time {}ms: Simulator ended for SRT [Q:{}]".format(time, getQueueFormatted(ready_queue_formatted)))
    
    global average_CPU_burst
    average_CPU_burst = total_CPU_burst_time/total_CPU_burst_count
    
    global average_wait_time
    total_wait_time = 0
    for i in process_list_copy:
        total_wait_time += sum(i.burst_wait_list)
    average_wait_time = total_wait_time/total_CPU_burst_count
    
    global average_turnaround_time
    for i in range(len(process_list_copy)):
        total_turnaround_time += sum(process_list_copy[i].burst_wait_list) + sum(process_list[i].CPUlst)
    total_turnaround_time += total_cs_time    #NOTE im not entirely sure how to include context switch time. see turnaround time on page 6
    average_turnaround_time = total_turnaround_time/total_CPU_burst_count

    utilization = (total_CPU_burst_time/time)

def outputWriting(filename):
    f = open(filename, "a")

    f.write("Algorithm SRT\n")
    f.write("-- average CPU burst time: {:.3f} ms\n".format(average_CPU_burst))
    f.write("-- average wait time: {:.3f} ms\n".format(average_wait_time))
    f.write("-- average turnaround time: {:.3f} ms\n".format(average_turnaround_time))
    f.write("-- total number of context switches: {}\n".format(total_context_switches))
    f.write("-- total number of preemptions: {}\n".format(total_preemptions))
    f.write("-- CPU utilization: {:.3f}%\n".format(utilization))

    f.close()    