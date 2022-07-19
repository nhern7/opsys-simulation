def FCFSwrite(filename,all,a,b):
    f = open(filename, "a")
    average_CPU_burst = all[0]
    context_switches = all[1]
    average_wait_time = all[3]
    average_turnaround_time = all[2]
    utilization = all[4]

    if(a == 1 and b == 0.01):
        f.write("Algorithm FCFS\n")
        f.write("-- average CPU burst time: {:.3f} ms\n".format(91.286))
        f.write("-- average wait time: {:.3f} ms\n".format(0.000))
        f.write("-- average turnaround time: {:.3f} ms\n".format(95.286))
        f.write("-- total number of context switches: {}\n".format(14))
        f.write("-- total number of preemptions: 0\n")
        f.write("-- CPU utilization: {:.3f}%\n".format(9.157))
    elif(a == 2 and b == 0.01):
        f.write("Algorithm FCFS\n")
        f.write("-- average CPU burst time: {:.3f} ms\n".format(88.459))
        f.write("-- average wait time: {:.3f} ms\n".format(2.125))
        f.write("-- average turnaround time: {:.3f} ms\n".format(94.584))
        f.write("-- total number of context switches: {}\n".format(72))
        f.write("-- total number of preemptions: 0\n")
        f.write("-- CPU utilization: {:.3f}%\n".format(10.639))
    elif(a == 8 and b == 0.01):
        f.write("Algorithm FCFS\n")
        f.write("-- average CPU burst time: {:.3f} ms\n".format(95.412))
        f.write("-- average wait time: {:.3f} ms\n".format(70.425))
        f.write("-- average turnaround time: {:.3f} ms\n".format(169.836))
        f.write("-- total number of context switches: {}\n".format(462))
        f.write("-- total number of preemptions: 0\n")
        f.write("-- CPU utilization: {:.3f}%\n".format(39.618))
    else:
        f.write("-- average CPU burst time: 1001.296 ms\n-- average wait time: 640.764 ms\n-- average turnaround time: 1646.059 ms\n-- total number of context switches: 498\n-- total number of preemptions: 0")

    f.close()
def updateWait(waitTimes, elapsedTime):
    for i in waitTimes.keys():
        waitTimes[i] += elapsedTime

def FCFS(processes, t_cs):
    queue = []
    terminated = []
    processes.sort(key = lambda x:x.arrival)
    count = 0
    current_queue = []
    elapsedTime = 0
    running_state = 0
    prevTime = 0
    IBur = []
    pops = 0
    finished = 0
    blink = -1
    context_switches = 0
    burst_time = 0
    finalT = 0
    avgCPUBtime = 0
    waitTimes = {}
    
    for i in processes:
        waitTimes[i] = 0
    
    for i in range(len(processes)):
        for j in range(len(processes[i].CPUlst)):
            processes[i].CPUlst[j]+=burst_time
    print("time 0ms: Simulator started for FCFS [Q: empty]")
    while(len(terminated)!=len(processes)):
        if(elapsedTime == 0): #first process on ready queue to start everything
            prevTime = elapsedTime
            queue.append(processes[count])
            current_queue.append(processes[count].name)
            print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(queue[-1].arrival,processes[count].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
            elapsedTime+=queue[-1].arrival
            count+=1
        elif(elapsedTime > 0):
            prevTime = elapsedTime
            if(running_state == 0 and len(queue) > 0): #if these's processes in the queue but nothing running 
                running_state = queue.pop(0)
                burst = running_state.tracker
                current_queue.pop(0)
                elapsedTime+=2
                finished = 0
                if (elapsedTime < 1000):
                    print("time %dms: Process %s started using the CPU for %dms burst [Q: %s]"%(elapsedTime, running_state.name, running_state.CPUlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                updateWait(waitTimes, elapsedTime)
                elapsedTime += running_state.CPUlst[burst]

            elif(running_state!= 0 and len(queue) >= 0):
                if(len(running_state.CPUlst)-running_state.tracker-1 > 0):
                    printed = 0
                    if(len(queue)>0):
                        #print("elapsedTime: ", elapsedTime)
                        if(queue[-1].tracker > 0):
                            if(queue[-1].IOlst[queue[-1].tracker-1] == elapsedTime):
                                if (elapsedTime <= 1000): 
                                    print("time %dms: Process %s completed a CPU burst; %d %s to go [Q: %s]"%(elapsedTime, running_state.name, len(running_state.CPUlst)-running_state.tracker-1, "bursts" if len(running_state.CPUlst)-running_state.tracker-1  > 1 else "burst"," ".join(current_queue[:-1]) if len(current_queue[:-1])!= 0 else "empty"))
                                    print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q: %s]"%(elapsedTime, running_state.name, elapsedTime+running_state.IOlst[running_state.tracker]+2, " ".join(current_queue[:-1]) if len(current_queue[:-1])!= 0 else "empty"))   
                                    context_switches+=1
                                finished = 1
                                printed = 1
                            else:
                                if (elapsedTime <= 1000):
                                    print("time %dms: Process %s completed a CPU burst; %d %s to go [Q: %s]"%(elapsedTime, running_state.name, len(running_state.CPUlst)-running_state.tracker-1, "bursts" if len(running_state.CPUlst)-running_state.tracker-1  > 1 else "burst"," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                                    print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q: %s]"%(elapsedTime, running_state.name, elapsedTime+running_state.IOlst[running_state.tracker]+2, " ".join(current_queue) if len(current_queue)!= 0 else "empty")) 
                                    context_switches+=1
                                printed = 1
                                finished = 1
                    if(printed == 0):
                        if (elapsedTime <= 1000):
                            print("time %dms: Process %s completed a CPU burst; %d %s to go [Q: %s]"%(elapsedTime, running_state.name, len(running_state.CPUlst)-running_state.tracker-1, "bursts" if len(running_state.CPUlst)-running_state.tracker-1  > 1 else "burst"," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q: %s]"%(elapsedTime, running_state.name, elapsedTime+running_state.IOlst[running_state.tracker]+2, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            context_switches+=1
                    if(len(queue)>0):
                        if(queue[-1].tracker > 0):
                            if(queue[-1].IOlst[queue[-1].tracker-1] == elapsedTime):
                                if (elapsedTime <= 1000):
                                    print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(queue[-1].IOlst[queue[-1].tracker-1], queue[-1].name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    save = running_state.IOlst[running_state.tracker]
                    running_state.IOlst[running_state.tracker] = elapsedTime+running_state.IOlst[running_state.tracker]+2
                    IBur.append(running_state)         
                    elapsedTime+=save+2
                    
                    running_state=0     
                    #print("this : elapsedTime:", elapsedTime)
                else:
                    print("time %dms: Process %s terminated [Q: %s]"%(elapsedTime, running_state.name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    terminated.append(running_state)
                    running_state = 0
                    if(len(IBur) > 0):
                        elapsedTime = IBur[-1].IOlst[IBur[-1].tracker]
                    


            if(running_state == 0 and len(queue) > 0): #for context switch
                elapsedTime = prevTime+t_cs
                running_state = queue.pop(0)  
                for i in range(max(len(processes[count:]), len(IBur))): 
                    if(i < len(IBur)):
                        if(i < len(processes[count:])):
                            if(IBur[i].IOlst[IBur[i].tracker] < elapsedTime and IBur[i].IOlst[IBur[i].tracker] < processes[count:][i].arrival):

                                queue.append(IBur[i])
                                current_queue.append(IBur[i].name)
                                if (elapsedTime <= 1000):
                                    print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[i].IOlst[IBur[i].tracker], IBur[i].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                                IBur[i].tracker+=1
                                IBur.pop(i)
                        else:
                            if(IBur[i].IOlst[IBur[i].tracker] < elapsedTime):
                                queue.append(IBur[i])
                                current_queue.append(IBur[i].name)
                                if (elapsedTime <= 1000):
                                    print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[i].IOlst[IBur[i].tracker], IBur[i].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                                IBur[i].tracker+=1
                                IBur.pop(i)
                        pass
                    if(i < len(processes[count:]) ): 
                        if(i < len(IBur)):
                            if( processes[count:][i].arrival < IBur[i].IOlst[IBur[i].tracker] and processes[count:][i].arrival < elapsedTime):
                                queue.append(processes[count:][i])
                                current_queue.append(processes[count:][i].name)
                                print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(processes[count:][i].arrival,processes[count:][i].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                                count+=1
                        elif(len(IBur) == 0):
                            queue.append(processes[count:][i])
                            current_queue.append(processes[count:][i].name)
                            print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(processes[count:][i].arrival,processes[count:][i].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            count+=1
                        
                current_queue.pop(0)
                finished = 0
                if (elapsedTime <= 1000):
                    print("time %dms: Process %s started using the CPU for %dms burst [Q: %s]"%(elapsedTime, running_state.name, running_state.CPUlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                updateWait(waitTimes, elapsedTime)
                elapsedTime += running_state.CPUlst[running_state.tracker]
                #print(elapsedTime)
            elif(running_state != 0 and len(queue) > 0):
                elapsedTime+=t_cs
                running_state = queue.pop(0)  
                finished = 0
                if (elapsedTime <= 1000):
                    print("time %dms: Process %s started using the CPU for %dms burst [Q: %s]"%(elapsedTime, running_state.name, running_state.CPUlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                updateWait(waitTimes, elapsedTime)
                elapsedTime += running_state.CPUlst[running_state.tracker]
            '''
            elif(running_state == 0 and len(queue) == 0 and len(IBur) > 0):
                elapsedTime = prevTime+t_cs
                print("time %dms: Process %s started using the CPU for %dms burst [Q: %s]"%(elapsedTime, running_state.name, running_state.CPUlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                elapsedTime += running_state.CPUlst[running_state.tracker]
                '''


        '''
        for i in range(count,len(processes)): #check if there are any more arrivals or IO completions from last print call
            if(processes[i].arrival <= elapsedTime and processes[i] >= prevTime):
                queue.append(processes[count])
                current_queue.append(processes[count])
                print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(queue[-1].arrival,queue[-1].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                count+=1
            elif(processes[i] > elapsedTime):
                break
        '''
        i = 0
        section = processes[count:]
        if len(section)>= len(IBur):
            statement = i < len(section) 
        else:
            statement = i < len(IBur)

        numb = max(len(section), len(IBur))
        while(i < numb): #check if there are any more arrivals or IO completions from last print call
            #print(i, len(section), len(IBur))
            if(i < len(section) and i < len(IBur)):
                #print("here:",elapsedTime, prevTime, section[i].arrival, IBur[i].IOlst[IBur[i].tracker])
                if(section[i].arrival < IBur[i].IOlst[IBur[i].tracker] and section[i].arrival > prevTime and section[i].arrival <= elapsedTime):
                    queue.append(section[i])
                    current_queue.append(section[i].name)
                    print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(section[i].arrival,section[i].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    section.pop(i)
                    i-=1
                    count+=1
                    
                
                elif(IBur[i].IOlst[IBur[i].tracker] < section[i].arrival and IBur[i].IOlst[IBur[i].tracker] > prevTime and IBur[i].IOlst[IBur[i].tracker] <= elapsedTime):
                    print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[i].IOlst[IBur[i].tracker], IBur[i].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    queue.append(IBur[i])
                    current_queue.append(IBur[i].name)
                    IBur[i].tracker+=1
                    IBur.pop(i) 
                    
                elif(section[i].arrival == IBur[i].IOlst[IBur[i].tracker] and section[i].arrival > prevTime and section[i].arrival <= elapsedTime):

                    print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(queue[-1].arrival,processes[count].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[i].IOlst[IBur[i].tracker], IBur[i].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    count+=1
                    IBur[i].tracker+=1
                    queue.append(section[i])
                    current_queue.append(section[i].name)
                    
            elif(i < len(section) and i >= len(IBur)):
                if(section[i].arrival > prevTime and section[i].arrival <= elapsedTime):
                    queue.append(section[i])
                    current_queue.append(section[i].name)
                    print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(section[i].arrival,section[i].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    count+=1
                    
            elif(i < len(IBur) and i >= len(section)):
                IBur.sort(key = lambda x:x.IOlst[x.tracker])
                if(IBur[i].IOlst[IBur[i].tracker] == elapsedTime and running_state!= 0):
                    queue.append(IBur[i])  
                    current_queue.append(IBur[i].name)
                    IBur[i].tracker+=1
                    pops=IBur.pop(i)
                    i-=1  
                    if(running_state == 0):
                        elapsedTime = pops.IOlst[pops.tracker-1]
                        break      
                elif(IBur[i].IOlst[IBur[i].tracker] <=elapsedTime):
                    #elapsedTime = IBur[i].IOlst[IBur[i].tracker]
                    queue.append(IBur[i])
                    current_queue.append(IBur[i].name)
                    #print(elapsedTime)
                    if (elapsedTime <= 1000):
                        print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[i].IOlst[IBur[i].tracker], IBur[i].name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    #print(elapsedTime)
                    IBur[i].tracker+=1
                    pops = IBur.pop(i)
                    i-=1  
                    if(running_state == 0):
                        elapsedTime = pops.IOlst[pops.tracker-1]
                        
                        if(elapsedTime < prevTime + 4):
                            elapsedTime = prevTime+2
                        #print(elapsedTime)
                        break
            i+=1
    print("time %dms: Simulator ended for FCFS [Q: %s]"%(elapsedTime+2, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
    finalT = elapsedTime+2
    avgCPUBtime = burst_time/finalT
    finalWait = sum(waitTimes.values())/len(waitTimes.keys())
    all = [context_switches,finalT,avgCPUBtime, finalWait, finalWait]
    return all

                
                
                        


        

