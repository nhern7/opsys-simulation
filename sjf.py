import process
import math 

' SHORTEST JOB FIRST '

def sjf(processes, alpha):
    next_p = ''
    current_p = ''
    context_switches = 0
    queue = [] # the entire process
    io_process = {}
    running = [False, '', '', '']
    processes.sort(key = lambda x : x.numCPUBursts)
    arrival_times = {}
    process_stuff = {}
    for i in range(len(processes)):
        process_stuff[processes[i].name] = processes[i]
    for i in range(len(processes)):
        arrival_times[processes[i].arrival] = processes[i].name
    current_queue = [] # just the name
    elapsedTime = 0
    print("time 0ms: Simulator started for SJF [Q: empty]")
    while True:
        if (len(process_stuff.keys())==0):
            print("time {}ms: Simulator ended for SJF [Q: empty]".format(elapsedTime+1))
            break
        if (elapsedTime in arrival_times.keys()):
            #print(arrival_times.keys())
            queue.append(process_stuff[arrival_times[elapsedTime]])
            current_queue.append(arrival_times[elapsedTime])
            queue.sort(key = lambda x : x.numCPUBursts)
            current_queue = sorted(current_queue)
            if (elapsedTime <= 1000):
                print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q: {}]".format(elapsedTime, arrival_times[elapsedTime], process_stuff[arrival_times[elapsedTime]].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
        if (running[0]):
            if (running[1]==elapsedTime):
            # CPU burst started
                current_p = running[3]
                if (elapsedTime <= 1000):
                    print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, (running[2]-running[1]), " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
            elif (running[2]==elapsedTime): 
            # CPU burst finished
                if (len(process_stuff[running[3]].CPUlst)==0): # process completely finished, no more CPU bursts
                    print("time {}ms: Process {} terminated [Q: {}]".format(elapsedTime, running[3], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    del process_stuff[running[3]]
                else: # process still has CPU bursts to complete
                    if (elapsedTime <= 1000):
                        if (process_stuff[running[3]].numCPUBursts > 1):
                            print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, process_stuff[current_p].numCPUBursts, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                        else:
                            print("time {}ms: Process {} (tau {}ms) completed a CPU burst; 1 burst to go [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    # update tau after CPU burst finished
                    old = process_stuff[current_p].tau
                    process_stuff[current_p].tau = math.ceil(process.CPUguess(process_stuff[current_p].tau, (running[2] - running[1]), alpha))
                    if (elapsedTime <= 1000):
                        print("time {}ms: Recalculated tau for process {}: old tau {}ms; new tau {}ms [Q: {}]".format(elapsedTime, running[3], old, process_stuff[current_p].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    # switch to CPU to IO
                    io_process[elapsedTime + process_stuff[running[3]].IOlst[0] + 2] = process_stuff[running[3]].name
                    t = elapsedTime + process_stuff[running[3]].IOlst[0] + 2
                    process_stuff[running[3]].IOlst.pop(0)
                    if (elapsedTime <= 1000):
                        print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q: {}]".format(elapsedTime, running[3], t, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
            elif (elapsedTime==(running[2]+2)):
                running[0] = False
        
        if (elapsedTime in io_process.keys()):
            #print("hi")
            queue.append(process_stuff[io_process[elapsedTime]])
            current_queue.append(io_process[elapsedTime])
            queue.sort(key = lambda x : x.numCPUBursts)
            current_queue = sorted(current_queue)
            if (elapsedTime <= 1000):
                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q: {}]".format(elapsedTime, io_process[elapsedTime], process_stuff[io_process[elapsedTime]].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
        
        if (not running[0] and len(queue)>0):
            next_p = queue[0]
            queue.pop(0)
            current_queue.pop(0)
            running[0] = True
            running[1] = elapsedTime + 2
            running[2] = elapsedTime + (process_stuff[next_p.name]).CPUlst[0] + 2 
            running[3] = next_p.name
            process_stuff[next_p.name].numCPUBursts-=1
            process_stuff[next_p.name].CPUlst.pop(0)
            context_switches+=1
        elapsedTime+=1
       # print(elapsedTime)