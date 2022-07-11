def FCFS(processes):
    queue = []
    terminated = []
    processes.sort(key = lambda x:x.arrival)
    count = 0
    current_queue = []
    elapsedTime = 0
    print("time 0ms: Simulator started for FCFS [Q: empty]")
    while(len(terminated)!=len(processes)):
        if(elapsedTime == 0): #first process on ready queue to start everything
            queue.append(processes[count])
            current_queue.append(processes[count].name)
            print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(queue[-1].arrival,processes[count].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
            elapsedTime+=queue[-1].arrival
            count+=1
        #elif(elapsedTime > 0): #it takes 2ms for process to run, check if any other arrivals happen in that time







        if(queue[0].tracker == 0):
            
            
        else:
            print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%())
            elapsedTime+= 
        if(len(processes) > 1):
            count+=1
            if(processes[count].arrival < processes[count-1]+2):
                print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(processes[count].arrival,processes[count].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                elapsedTime = processes[count].arrival
                queue.append(processes[count])
                if(len(processes) > 2):
                    count+=1
        current_queue.pop(0)
        running_state = queue.pop(0)
        elapsedTime+=2
        print("time %dms: Process %s started using the CPU for %dms burst [Q: %s]"%(elapsedTime, running_state.name, running_state.CPUlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
        elapsedTime+=running_state.CPUlst[running_state.tracker]
        print("time %dms: Process %s completed a CPU burst; %d bursts to go [Q: %s]"%(elapsedTime, running_state.name, len(running_state.CPUlst)-running_state.tracker-1    , " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
        print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q: %s]"%(elapsedTime, running_state.name, elapsedTime+running_state.IOlst[running_state.tracker]+2, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
        
        running_state.tracker+=1

        if(running_state.tracker < len(running_state.CPUlst)):
            queue.append(running_state)
            print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(elapsedTime, ))
        else:
            print("time %dms: Process %s terminated [Q: %s]"%(elapsedTime+running_state.CPUlst[running_state.tracker], running_state.name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
            terminated.append(running_state)
            



        

