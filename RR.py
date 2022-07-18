from cProfile import run
from optparse import check_builtin


def checkOtherTimes(processes, queue, current_queue, IBur, endWindow, elapsedTimel, running_state, start, eTime):
    
    eTime[-1] = endWindow
    IBur.sort(key = lambda x:x.IOlst[x.tracker])
    
    while(True):
        if(len(processes) > 0 and len(IBur) > 0):
            if(processes[0].arrival <= endWindow and processes[0].arrival < IBur[0].IOlst[IBur[0].tracker]):
                elapsedTimel[0]=processes[0].arrival
                queue.append(processes[0])
                current_queue.append(processes[0].name)
                print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(processes[0].arrival, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                processes.pop(0)
            elif( IBur[0].IOlst[IBur[0].tracker] < endWindow and processes[0].arrival > IBur[0].IOlst[IBur[0].tracker]):
                elapsedTimel[0]=processes[0].arrival
                queue.append(IBur[0])
                current_queue.append(IBur[0].name)
                print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[0].IOlst[IBur[0].tracker], IBur[0].name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                IBur[0].tracker+=1
                IBur.pop(0)
            elif( IBur[0].IOlst[IBur[0].tracker] <= endWindow and processes[0].arrival == IBur[0].IOlst[IBur[0].tracker]):
                elapsedTimel[0]=processes[0].arrival
                queue.append(processes[0])
                current_queue.append(processes[0].name)
                processes.pop(0)
                print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%(queue[-1].arrival,processes[0].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                queue.append(IBur[0].IOlst[IBur[0].tracker])
                current_queue.append(IBur[0].name)
                print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[0].IOlst[IBur[0].tracker], IBur[0].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                IBur[0].tracker+=1
                IBur.pop(0)
            else:
                break
        elif(len(processes) > 0  and len(IBur) == 0):
            if(processes[0].arrival <= endWindow):
                elapsedTimel[0]=processes[0].arrival
                queue.append(processes[0])
                current_queue.append(processes[0].name)
                print("time %dms: Process %s arrived; added to ready queue [Q: %s ]"%(processes[0].arrival, processes[0].name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                processes.pop(0)
            else:
                break
        elif(len(IBur) > 0 and len(processes) == 0):
            if(IBur[0].IOlst[IBur[0].tracker] < endWindow):
                elapsedTimel[0]=IBur[0].IOlst[IBur[0].tracker]
                queue.append(IBur[0])
                current_queue.append(IBur[0].name)
                print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[0].IOlst[IBur[0].tracker], IBur[0].name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                IBur[0].tracker+=1
                IBur.pop(0)
                if(len(queue) == 1 and running_state == 0):
                    if(len(IBur) > 0):
                        while(True):
                            if(len(IBur) > 0 and IBur[0].tracker < len(IBur[0].IOlst)):
                                if(IBur[0].IOlst[IBur[0].tracker] <= elapsedTimel[0] + start):
                                    queue.append(IBur[0])
                                    current_queue.append(IBur[0].name)
                                    print("time %dms: Process %s completed I/O; added to ready queue [Q: %s]"%(IBur[0].IOlst[IBur[0].tracker], IBur[0].name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                                    IBur[0].tracker+=1
                                    IBur.pop(0)
                                else:
                                    break
                            else:
                                break  
                        eTime[0] = elapsedTimel[0] + start              
                    break
            else:
                break
        else:
            
            break
            

def RR(processes, t_cs, t_slice):
    queue = []
    terminated = []
    processes.sort(key = lambda x:x.arrival)
    total = len(processes)
    count = 0
    current_queue = []
    elapsedTime = 0
    running_state = 0
    endWindow = 0
    IBur = []
    pops = 0
    finished = 0
    blink = -1
    cTime = [-1]
    eTime = [-1]
    endCPU = -1
    switch = t_cs/2
    start = t_cs/2
    
    print("time %dms: Simulator started for Round Robin [Q: %s]"%(elapsedTime, "empty"))
    while(len(terminated)!=total):
        cTime[0] = elapsedTime
        if(elapsedTime == 0):
            queue.append(processes.pop(0))
            current_queue.append(queue[-1].name)
            elapsedTime+=queue[-1].arrival
            print("time %dms: Process %s arrived; added to ready queue [Q: %s]"%( elapsedTime, queue[-1].name," ".join(current_queue) if len(current_queue)!= 0 else "empty"))
            endWindow = elapsedTime + start
            eTime[-1] = endWindow
        elif(elapsedTime>0):

            if(running_state == 0 and len(queue) > 0): #switch will happen here 
                if(endWindow != eTime[-1]):
                    endWindow = eTime[-1]
                checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                
                
                running_state = queue.pop(0)
                
                current_queue.pop(0)
                print("Ltime %dms: Process %s started using the CPU for %dms burst [Q: %s]"%(endWindow, running_state.name, running_state.CPUlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                elapsedTime = endWindow
                endWindow += t_slice
                
                if(endWindow > elapsedTime + running_state.CPUlst[running_state.tracker]):
                    endWindow = elapsedTime + running_state.CPUlst[running_state.tracker]
                    checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)

                    print("kktime %dms: Process %s completed a CPU burst; %d %s to go [Q: %s]"%(endWindow, running_state.name, len(running_state.CPUlst)-running_state.tracker-1, "bursts" if len(running_state.CPUlst)-running_state.tracker-1  > 1 else "burst", " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q: %s]"%(endWindow, running_state.name, endWindow + switch + running_state.IOlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    running_state.IOlst[running_state.tracker] += endWindow+switch
                    IBur.append(running_state)
                    elapsedTime = endWindow
                    if(len(queue) == 0):
                        endWindow = running_state.IOlst[running_state.tracker]
                    else:
                        endWindow += switch
                        
                        checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                        endWindow+=start
                        checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                    
                    running_state = 0
            elif(running_state == 0 and len(queue) == 0):   
                if(len(IBur) > 0):
                    endWindow += start 
                    checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                    if(len(queue) ==1):
                        running_state = queue.pop(0)
                        endWindow = cTime[0]+start  
                        current_queue.pop(0)
                        print("Btime %dms: Process %s started using the CPU for %dms burst [Q: %s]"%(endWindow, running_state.name, running_state.CPUlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                        elapsedTime = endWindow
                        if(endWindow+t_slice > endWindow+running_state.CPUlst[running_state.tracker]):
                            endWindow += running_state.CPUlst[running_state.tracker]
                            running_state.CPUlst[running_state.tracker] = 0
                            checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                            print("time %dms: Process %s completed a CPU burst; %d %s to go [Q: %s]"%(endWindow, running_state.name, len(running_state.CPUlst)-running_state.tracker-1, "bursts" if len(running_state.CPUlst)-running_state.tracker-1  > 1 else "burst", " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q: %s]"%(endWindow, running_state.name, endWindow + switch + running_state.IOlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            
                            running_state.IOlst[running_state.tracker] += endWindow + switch
                            IBur.append(running_state)
                            if(len(queue) == 0):
                                elapsedTime = endWindow
                                endWindow =  running_state.IOlst[running_state.tracker]  
                                running_state = 0   
                            else:
                                endWindow += switch
                                checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                                endWindow+=start
                                checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                                running_state = 0

                        else:
                            endWindow += t_slice
                        
            elif(running_state != 0): 
                checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                if(len(running_state.CPUlst)-running_state.tracker-1 >= 0):
                    if(len(queue) == 0):
                        running_state.CPUlst[running_state.tracker] -= t_slice
                        if(running_state.CPUlst[running_state.tracker] != 0):
                            print("time %dms: Time slice expired; no preemption because ready queue is empty [Q: empty]"%(endWindow))
                        elapsedTime = endWindow
                        endWindow +=  t_slice


                        if(endWindow > elapsedTime + running_state.CPUlst[running_state.tracker] and len(running_state.CPUlst)-running_state.tracker-1  > 0):  
                            endWindow = elapsedTime + running_state.CPUlst[running_state.tracker]
                            running_state.CPUlst[running_state.tracker] = 0
                            checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                            print("Jtime %dms: Process %s completed a CPU burst; %d %s to go [Q: %s]"%(endWindow, running_state.name, len(running_state.CPUlst)-running_state.tracker-1, "bursts" if len(running_state.CPUlst)-running_state.tracker-1  > 1 else "burst", " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q: %s]"%(endWindow, running_state.name, endWindow + switch + running_state.IOlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            running_state.IOlst[running_state.tracker] += endWindow + switch
                            IBur.append(running_state)
                            elapsedTime = endWindow
                            if(len(queue) == 0):
                                endWindow =  running_state.IOlst[running_state.tracker]    
                            else:
                                endWindow += switch
                                checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                                endWindow+=start
                                checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                            running_state = 0
                    elif(len(queue)>0):
                        running_state.CPUlst[running_state.tracker] -= t_slice
                        if(running_state.CPUlst[running_state.tracker] != 0):
                            print("time %dms: Time slice expired; process %s preempted with %dms remaining [Q: %s]"%(endWindow, running_state.name, running_state.CPUlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            elapsedTime = endWindow
                            endWindow += switch
                            checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                            queue.append(running_state)
                            current_queue.append(running_state.name)
                            
                        elif(running_state.CPUlst[running_state.tracker] == 0):
                            print("Ftime %dms: Process %s completed a CPU burst; %d %s to go [Q: %s]"%(endWindow, running_state.name, len(running_state.CPUlst)-running_state.tracker-1, "bursts" if len(running_state.CPUlst)-running_state.tracker-1  > 1 else "burst", " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            print("time %dms: Process %s switching out of CPU; will block on I/O until time %dms [Q: %s]"%(endWindow, running_state.name, endWindow + switch + running_state.IOlst[running_state.tracker], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            running_state.IOlst[running_state.tracker] += endWindow + switch
                            IBur.append(running_state)
                            elapsedTime = endWindow
                            endWindow+=switch 
                        checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                        endWindow+=start
                        checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                        running_state = 0
                    if(running_state != 0):
                        if(endWindow > elapsedTime + running_state.CPUlst[running_state.tracker] and len(running_state.CPUlst)-running_state.tracker-1 == 0):
                            endWindow = elapsedTime + running_state.CPUlst[running_state.tracker]
                            running_state.CPUlst[running_state.tracker] -= t_slice
                            checkOtherTimes(processes, queue,current_queue,IBur,endWindow, cTime,running_state, start, eTime)
                            print("time %dms: Process %s terminated [Q: %s]"%(endWindow, running_state.name, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                            terminated.append(running_state)
                            running_state = 0    
                

                


                    
        