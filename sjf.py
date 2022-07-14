import process
import math 

' SHORTEST JOB FIRST '

def sjf(processes, alpha):
    next_p = ''
    current_p = ''
    context_switches = 0
    queue = [] # the entire process
    # io_proccess = []
    # terminated = []
    running = [False, '', '', '']
    processes.sort(key = lambda x : x.numCPUBursts)
    arrival_times = {}
    process_stuff = {}
    for i in range(len(processes)):
        process_stuff[processes[i]] = processes[i].name
    for i in range(len(processes)):
        arrival_times[processes[i]] = processes[i].arrival
    current_queue = [] # just the name
    elapsedTime = 0
    print("time 0ms: Simulator started for SJF [Q: empty]")
    while True:
        if (len(process_stuff.keys())==0):
            print("time {}ms: Simulator ended for SJF [Q: empty]".format(elapsedTime+1))
            break

        if (elapsedTime in arrival_times.key()):
            queue.append(arrival_times[elapsedTime][0])
            current_queue.append(arrival_times[elapsedTime][0].name)
            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q: {}]".format(elapsedTime, arrival_times[elapsedTime][0].name, arrival_times[elapsedTime][0].tau, arrival_times[elapsedTime][0].name))

        if (running[0]):
            if (running[1]==elapsedTime):
            # CPU burst startes
                current_p = running[3]
                print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst".format(elapsedTime, running[3], process_stuff[current_p].tau, (running[2]-running[1])))
            elif (running[2]==elapsedTime): 
            # CPU burst finished
                if (len(process_stuff[running[3]].CPUlst)==0): # process completely finished, no more CPU bursts
                    print("time {}ms: Process {} terminated [Q: {}]".format(elapsedTime, running[3], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    del process_stuff[running[3]]
                else: # process still has CPU bursts to complete
                    if (process_stuff[running[3]].numCPUBursts > 1):
                        print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, process_stuff[current_p].numCPUBursts, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    else:
                        print("time {}ms: Process {} (tau {}ms) completed a CPU burst; 1 burst to go [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                # update tau after CPU burst finished
                old = process_stuff[current_p].tau
                process_stuff[current_p].tau = math.ceil(process.CPUguess(process_stuff[current_p].tau, (running[2] - running[1]), alpha))
                print("time {}ms: Recalculated tau for process {}: old tau {}ms; new tau {}ms [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
            elif (elapsedTime==(running[2]+2)):
                running[0] = False

        if (not running[0] and len(queue)>0):
            next_p = queue[0]
            queue.pop(0)
            running[0] = True
            running[1] = elapsedTime + 2
            running[2] = elapsedTime + process_stuff[next_p].remaining + 2 
            running[3] = next_p
            process_stuff[next_p].numCPUBursts-=1
            process_stuff[next_p].CPUList.pop(0)
            context_switches+=1
        elapsedTime+=1

    print("time {}ms: Simulator ended for SJF [Q: empty]".format(elapsedTime))

    '''
    file.write('Algorithm SJF\n')
    file.write(f'-- average CPU burst time: ms\n')
    file.write(f'-- average wait time: ms\n')
    file.write(f'-- average turnaround time: ms\n')
    file.write(f'-- total number of context switches: \n')
    file.write(f'-- total number of preemptions: 0\n')
    file.write(f'-- CPU utilization: \n')
    '''