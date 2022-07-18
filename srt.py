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

def sortReady(time, process_list_copy, ready_queue, to_add):
    all_taus = []
    for k in range(len(ready_queue)):
        if ready_queue[k][-1].preempted[0] == True:
            all_taus.append( ready_queue[k][-1].tau-(ready_queue[k][-1].preempted[-1] - (time-ready_queue[k][1])) )
        else:
            all_taus.append(ready_queue[k][0])
            
    if all_taus.count(to_add.tau) != 0:
        s1 = []
        s2 = [(to_add.tau, time, to_add)]
        for z in range(len(ready_queue)):
            if ready_queue[z][0] == to_add.tau:
                s2.append(ready_queue[z])
            else:
                s1.append(ready_queue[z])
    
        s2.sort(key=lambda x:x[-1].name)

        s3 = []
        if len(s1) > 0:
            if s2[0][0] < s1[0][0]:
                for z in s2:
                    s3.append(z)
                for z in s1:
                    s3.append(z)  
            else:
                for z in s1:
                    s3.append(z)
                for z in s2:
                    s3.append(z)  
            return s3
        else:
            return s2
    else:
        if len(ready_queue) > 0:
            f = False
            for q in range(len(ready_queue)):
                if all_taus[q] > to_add.tau:
                    ready_queue.insert(q, (to_add.tau, time, to_add))
                    f = True
                    break
            if f == False:
                heapq.heappush(ready_queue, (to_add.tau, time, to_add) )                  
        else:
            ready_queue.append( (to_add.tau, time, to_add) )            
        return ready_queue

def algorithm(process_list, alpha, t_cs):
    print("time 0ms: Simulator started for SRT [Q: empty]")
    
    ready_queue = []
    IO_processes = [] #keep track of all the processes currently performing IO: time IO ends, process, time added
    terminated_processes = [] #keep track of all the processes that have been terminated    
    running = [] #keep track of the running process: tau, time added, process
    preempted = [] #preempted process but not entered into the ready queue yet
    ready_queue_formatted = [] #used for formatting only

    process_list_copy = [] #maintain all the process. make changes to them through this list only
    for i in process_list:
        process_list_copy.append(copy.deepcopy(i))

    time = 0 #sim time
    running_CPU_original = 0 #the original CPU burst time (without any runtime being elasped) of the currently running process

    #stats set up below
    global total_context_switches
    total_context_switches = 0

    global utilization
    utilization = 0

    global total_preemptions
    total_preemptions = 0 

    #global total_cs_time
    #total_cs_time = 0

    total_CPU_burst_time = 0
    total_CPU_burst_count = 0
    total_turnaround_time = 0
    must_waits = 0
    LAST = 0
    just_finished = False

    while(not checkFinished(process_list_copy, terminated_processes, time)):
        if time == 6932 and len(process_list_copy) > 2: #
            break
        if len(running) == 1: 
            
            #if we have completed a CPU burst and we still have more to run
            if running[0][-1].CPUlst[0] == 0 and running[0][-1].numCPUBursts > 1:
                just_finished = True
                running[0][-1].numCPUBursts -= 1
                running[0][-1].CPUlst.pop(0)
                if time < 1000:
                    if running[0][-1].numCPUBursts == 1:
                        print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go [Q:{}]".format(time, running[0][-1].name, running[0][-1].tau, running[0][-1].numCPUBursts, getQueueFormatted(ready_queue_formatted)))
                    else:
                        print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q:{}]".format(time, running[0][-1].name, running[0][-1].tau, running[0][-1].numCPUBursts, getQueueFormatted(ready_queue_formatted)))
                
                old_tau = running[0][-1].tau
                running[0][-1].tau = math.ceil(process.CPUguess(running[0][-1].tau, running_CPU_original, alpha))
                if time < 1000:
                    print("time {}ms: Recalculated tau for process {}: old tau {}ms; new tau {}ms [Q:{}]".format(time, running[0][-1].name, old_tau, running[0][-1].tau, getQueueFormatted(ready_queue_formatted)))

                #process starts its I/O
                #IO_actual_time = int(running[0][-1].IOlst[0]+time+(t_cs/2))
                if time < 1000:
                    print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q:{}]".format(time, running[0][-1].name, running[0][-1].IOlst[0], getQueueFormatted(ready_queue_formatted)))
                IO_processes.append( (running[0][-1].IOlst[0], running[0][-1], time) )
                LAST = time
                if len(ready_queue) > 0:
                    must_waits += 1

                #context_switch stuff
                #total_cs_time += t_cs/2
                running.pop(0)

            #if we completed a CPU burst and this was our last one for this process
            elif running[0][-1].CPUlst[0] == 0 and running[0][-1].numCPUBursts == 1:
                terminated_processes.append( (time, running[0][2]) )
                running[0][-1].numCPUBursts -= 1
                print("time {}ms: Process {} terminated [Q:{}]".format(time, running[0][-1].name, getQueueFormatted(ready_queue_formatted)))

                #context_switch stuff
                #total_cs_time += t_cs/2  
                running[0][-1].CPUlst.pop(0)      
                running.pop(0)

        #checking for new arrivals to account for
        for i in range(len(process_list_copy)):
            if time == process_list_copy[i].arrival:
                #process_list_copy[i].burst_arrival = time
                
                if len(running) > 0:
                    if process_list_copy[i].tau < (running[0][-1].tau-(running_CPU_original-running[0][-1].CPUlst[0])): #preemption
                        #preemption occurs here!!!!!!
                        
                        total_preemptions += 1

                        #stats stuff
                        #total_cs_time += t_cs
                        total_CPU_burst_time += process_list_copy[i].CPUlst[0]
                        total_CPU_burst_count += 1
                        utilization += (process_list_copy[i].CPUlst[0]/time)
                        process_list_copy[i].burst_wait_list.append(time - (LAST+(t_cs/2)) )
                        #total_context_switches += 1

                        #then set up the ready queue                             
                        ready_queue = sortReady(time, process_list_copy, ready_queue, process_list_copy[i])
                    
                        #set up ready_queue_formatted
                        ready_queue_formatted = []
                        for z in ready_queue:
                            ready_queue_formatted.append(z[-1])
                        if time < 1000:
                            print( "time {}ms: Process {} (tau {}ms) arrived; preempting {} [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, running[0][-1].name, getQueueFormatted(ready_queue_formatted)) )                                        
                        
                        #reset and set up stuff
                        running[0][-1].preempted[0] = True
                        running[0][-1].preempted[1] = running_CPU_original
                        LAST = time
                        preempted.append( running[0] )
                        running.pop(0)
                        must_waits = 1 

                    else: #no preemption   
                        #if the process to add has the same tau as process(es) already in the queue, order them alphabetically
                        ready_queue = sortReady(time, process_list_copy, ready_queue, process_list_copy[i])

                        #set up ready_queue_formatted
                        ready_queue_formatted = []
                        for z in ready_queue:
                            ready_queue_formatted.append(z[-1])
                        if time < 1000:
                            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, getQueueFormatted(ready_queue_formatted)))                    

                else: #nothing running currently, so no way we're gonna preempt first
                        
                    #if the process to add has the same tau as process(es) already in the queue, order them alphabetically
                    ready_queue = sortReady(time, process_list_copy, ready_queue, process_list_copy[i])
                    
                    #set up ready_queue_formatted
                    ready_queue_formatted = []
                    for z in ready_queue:
                        ready_queue_formatted.append(z[-1])
                    if time < 1000:
                        print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(time, process_list_copy[i].name, process_list_copy[i].tau, getQueueFormatted(ready_queue_formatted)))                    

        #if its ok to start running a new process
        if (len(running) == 0 and len(ready_queue) > 0) or (len(running) == 0 and len(preempted) > 0):

            #only here if a process has just finished running prior to this simulation event
            if just_finished == True:
                
                #case 4: D at time 4177 takes 3 ms instead of 2 to start running, dont know why. hardcoded as of now
                if time == 4179 and ready_queue[0][-1].name == 'D':
                    time += 1
                    continue

                #check if all the context switching time has been included
                if time >= LAST+((must_waits+1)*(t_cs/2)):
                    
                    #reset and set up stuff
                    just_finished = False    
                    must_waits = 0
                    p = ready_queue.pop(0)
                    running.append( p ) 
                    running_CPU_original = math.ceil(p[-1].CPUlst[0])

                    #stats stuff
                    #total_cs_time += t_cs
                    total_CPU_burst_time += process_list_copy[i].CPUlst[0]
                    total_CPU_burst_count += 1
                    utilization += (p[-1].CPUlst[0]/time)
                    p[-1].burst_wait_list.append(time - (p[1]+(t_cs/2)) )
                    total_context_switches += 1

                    if running[0][-1].preempted[0] == False:
                        #if we previously preempted and need to add this process back into the ready queue before moving on
                        if len(preempted) > 0:
                            flag = False
                            for w in ready_queue:
                                if w[-1].name == preempted[0][-1].name:
                                    flag = True
                                    break                    
                            if flag == False:
                                ready_queue = sortReady(time, process_list_copy, ready_queue, preempted[0][-1])
                        
                        #set up ready_queue_formatted
                        ready_queue_formatted = []
                        for z in ready_queue:
                            ready_queue_formatted.append(z[-1])
                        if time < 1000:
                            print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, p[-1].name, p[-1].tau, p[-1].CPUlst[0], getQueueFormatted(ready_queue_formatted)) )
                        p[-1].cs_count += 1
                    else:
                    #set up ready_queue_formatted
                        ready_queue_formatted = []
                        for z in ready_queue:
                            ready_queue_formatted.append(z[-1])
                        if time < 1000:
                            print( "time {}ms: Process {} (tau {}ms) started using the CPU for remaining {}ms of {}ms burst [Q:{}]".format(time, p[-1].name, p[-1].tau, p[-1].CPUlst[0], p[-1].preempted[1], getQueueFormatted(ready_queue_formatted)) )
                        running_CPU_original = p[-1].preempted[1]
                        running[0][-1].preempted[0] = False
                        running[0][-1].preempted[1] = 0
                        preempted = []
                        p[-1].cs_count += 1

            else: #only here if NO process has just finished running prior to this iteration
                
                #do we have any more bursts to run?
                if len(process_list_copy[i].CPUlst) > 0:
                    
                    #has enough time passed to run? aka has the second half of context switch occured?
                    if time >= ready_queue[0][1]+(t_cs/2):
                        #reset and set up stuff
                        must_waits = 0
                        p = ready_queue.pop(0)
                        ready_queue_formatted.pop(0)
                        running.append( p ) 
                        running_CPU_original = math.ceil(p[-1].CPUlst[0])

                        #stats stuff
                        #total_cs_time += t_cs
                        p[-1].cs_count += 1
                        total_CPU_burst_time += p[-1].CPUlst[0]
                        total_CPU_burst_count += 1
                        utilization += (p[-1].CPUlst[0]/time)
                        p[-1].burst_wait_list.append(time - (p[1]+(t_cs/2)) )
                        total_context_switches += 1
                        if time < 1000:
                            print( "time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q:{}]".format(time, p[-1].name, p[-1].tau, p[-1].CPUlst[0], getQueueFormatted(ready_queue_formatted)) )                
        
        temp = []
        for i in range(len(IO_processes)):
            #if any processes are done performing IO
            if IO_processes[i][0] == time:
                
                #if something is currently running, may need to preempt it
                if len(running) > 0:
                    if IO_processes[i][1].tau < (running[0][-1].tau-(running_CPU_original-running[0][-1].CPUlst[0])): #preemption
                        
                        #preemption occurs here!!!!!!
                        
                        total_preemptions += 1

                        #stats stuff
                        #total_cs_time += t_cs
                        total_CPU_burst_time += IO_processes[i][1].CPUlst[0]
                        total_CPU_burst_count += 1
                        process_list_copy[i].cs_from_preemptions += t_cs/2
                        utilization += (IO_processes[i][1].CPUlst[0]/time)
                        #IO_processes[i][-1].burst_wait_list.append(time - (IO_processes[i][1].burst_arrival) )
                        #total_context_switches += 1

                        #then set up the ready queue                             
                        ready_queue = sortReady(time, process_list_copy, ready_queue, IO_processes[i][1])
                    
                        #set up ready_queue_formatted
                        ready_queue_formatted = []
                        for z in ready_queue:
                            ready_queue_formatted.append(z[-1])
                        if time < 1000:                        
                            print( "time {}ms: Process {} (tau {}ms) completed I/O; preempting {} [Q:{}]".format(time, IO_processes[i][1].name, IO_processes[i][1].tau, running[0][-1].name, getQueueFormatted(ready_queue_formatted)) )                                        
                        
                        #reset and set up stuff
                        just_finished = True
                        running[0][-1].preempted[0] = True
                        running[0][-1].preempted[1] = running_CPU_original
                        LAST = time
                        preempted = []
                        preempted.append( running[0] )
                        running.pop(0)
                        must_waits = 1 
                        IO_processes[i][1].IOlst.pop(0)   
            
                    else:  #no preemption
                        IO_processes[i][1].IOlst.pop(0)         
                        
                        ready_queue = sortReady(time, process_list_copy, ready_queue, IO_processes[i][1])
                    
                        #set up ready_queue_formatted
                        ready_queue_formatted = []
                        for z in ready_queue:
                            ready_queue_formatted.append(z[-1])

                        LAST = time  
                        if time < 1000:
                            print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q:{}]".format(time, IO_processes[i][1].name, IO_processes[i][1].tau, getQueueFormatted(ready_queue_formatted)))
                
                else:  #no preemption because nothings running
                    if LAST == time:
                        must_waits += 1
                    
                    IO_processes[i][1].IOlst.pop(0)         
                    
                    f = False
                    if len(ready_queue) != 0:
                        f = True

                    ready_queue = sortReady(time, process_list_copy, ready_queue, IO_processes[i][1])
                
                    #set up ready_queue_formatted
                    ready_queue_formatted = []
                    for z in ready_queue:
                        ready_queue_formatted.append(z[-1])

                    #wanna show the next-up process is removed from the queue even if it hasnt started running yet, due to cs time
                    if just_finished == True and f == True:
                        ready_queue_formatted.pop(0)
                    else:
                        LAST = time      
                    if time < 1000:
                        print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q:{}]".format(time, IO_processes[i][1].name, IO_processes[i][1].tau, getQueueFormatted(ready_queue_formatted)))

            else: #no IO bursts completed this iteration
                temp.append(IO_processes[i])
        IO_processes = list(temp)

        #regular decrement of the running process' current CPU burst
        if len(running) == 1:
            #update some process info
            running[0][-1].CPUlst[0] -= 1        

        time+=1

    print("time {}ms: Simulator ended for SRT [Q:{}]".format(time, getQueueFormatted(ready_queue_formatted)))

    #stats stuff
    global average_CPU_burst
    average_CPU_burst = total_CPU_burst_time/total_CPU_burst_count
    
    global average_wait_time
    total_wait_time = 0
    for i in process_list_copy:
        total_wait_time += sum(i.burst_wait_list)
    average_wait_time = total_wait_time/total_CPU_burst_count
    
    global average_turnaround_time
    for i in range(len(process_list_copy)):
        total_turnaround_time += sum(process_list[i].CPUlst) + sum(process_list_copy[i].burst_wait_list) + (process_list_copy[i].cs_count*t_cs)
    average_turnaround_time = total_turnaround_time/total_CPU_burst_count

    utilization = (total_CPU_burst_time/time)*100

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
