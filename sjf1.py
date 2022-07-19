import process
import math 

' SHORTEST JOB FIRST '

def sjf(processes, alpha, filename):
   # analysis variable
    context_switches = 0
    cpu_burst_time = [0, 0]
    wait_time = 0
    useful_time = 0

    print("time 0ms: Simulator started for SJF [Q empty]")

    next_p = ''
    queue = [] # the entire process
    io_process = {}
    running = [False, '', '', '']
    processes.sort(key = lambda x : x.numCPUBursts)
    arrival_times = {}
    process_stuff = {}
    block_map = {}
    for i in range(len(processes)):
        process_stuff[processes[i].name] = processes[i]
    for i in range(len(processes)):
        arrival_times[processes[i].arrival] = processes[i].name
    current_queue = [] # just the name

    elapsedTime = 0
    running = [False, '', '', '']

    while True:
        old_queue = queue
        current_p = ''

        if (len(process_stuff.keys())==0):
            print("time {}ms: Simulator ended for SJF [Q empty]".format(elapsedTime+1))
            break
        if (running[0]):
            if (elapsedTime == running[1]):
            # CPU burst started
                current_p = running[3]
                cpu_burst_time[0] += running[2] - running[1]
                cpu_burst_time[1] += 1
                useful_time += running[2] - running[1]
                if (elapsedTime <= 1000):
                    print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, (running[2]-running[1]), " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
            if (elapsedTime == running[2]):
            # CPU burst finished
                current_p = running[3]
                if (len(process_stuff[running[3]].CPUlst)==0): # process completely finished, no more CPU bursts
                    print("time {}ms: Process {} terminated [Q: {}]".format(elapsedTime, running[3], " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    del process_stuff[running[3]]
                else: # process still has CPU bursts to complete
                    if (elapsedTime <= 1000):
                        if (process_stuff[running[3]].numCPUBursts > 1):
                            print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, process_stuff[current_p].numCPUBursts, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                        else:
                            print("time {}ms: Process {} (tau {}ms) completed a CPU burst; 1 burst to go [Q: {}]".format(elapsedTime, running[3], process_stuff[current_p].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    
                    #block = process_stuff[running[3]].name
                    block_time = process_stuff[running[3]].IOlst[0] + 2
                    process_stuff[running[3]].IOlst.pop(0)

                    old = process_stuff[current_p].tau
                    process_stuff[current_p].tau = math.ceil(process.CPUguess(process_stuff[current_p].tau, (running[2] - running[1]), alpha))
                    if (elapsedTime <= 1000):
                        print("time {}ms: Recalculated tau for process {}: old tau {}ms; new tau {}ms [Q: {}]".format(elapsedTime, running[3], old, process_stuff[current_p].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))

                    if (elapsedTime <= 1000):
                        print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms [Q: {}]".format(elapsedTime, running[3], elapsedTime+block_time, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))
                    block_map[process_stuff[running[3]].name] = elapsedTime + block_time, process_stuff[running[3]]
            if (elapsedTime == running[2]+2):
                running[0] = False

        for v in block_map.values():
            if (elapsedTime == v[0]):
                queue.append(v[1])
                queue.sort(key = lambda x : (x.numCPUBursts, x.name))
                current_queue.append(v[1].name)
                current_queue = sorted(current_queue)

                if (elapsedTime <= 1000):
                    print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue [Q: {}]".format(elapsedTime, v[1].name, v[1].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))

        # check if there is a process coming at this time
        if (elapsedTime in arrival_times.keys()):
            queue.append(process_stuff[arrival_times[elapsedTime]])
            current_queue.append(arrival_times[elapsedTime])
            queue.sort(key = lambda x : (x.numCPUBursts, x.name))
            current_queue = sorted(current_queue)
            if (elapsedTime <= 1000):
                print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q: {}]".format(elapsedTime, arrival_times[elapsedTime], process_stuff[arrival_times[elapsedTime]].tau, " ".join(current_queue) if len(current_queue)!= 0 else "empty"))

        # no process is running and there is at least one ready process
        if (not running[0] and len(queue)>0):
            next_p = queue[0]
            name = queue[0].name
            queue.pop(0)
            num = 0
            for i in range(len(current_queue)):
                if (name == current_queue[i]):
                    num = i
            current_queue.pop(num)
            running[0] = True
            running[1] = elapsedTime + 2
            running[2] = elapsedTime + (process_stuff[next_p.name]).CPUlst[0] + 2 
            running[3] = next_p.name
            process_stuff[next_p.name].numCPUBursts-=1
            process_stuff[next_p.name].CPUlst.pop(0)
            context_switches+=1

            if (current_p != '' and next_p != current_p):
                running[1] += 2
                running[2] += 2

        for p in set(old_queue).intersection(queue):
            wait_time += 1

        elapsedTime += 1

    average_cpu_burst_time = cpu_burst_time[0] / cpu_burst_time[1]
    average_wait_time = wait_time / cpu_burst_time[1]
    average_turnaround_time = average_cpu_burst_time + average_wait_time + 4
    CPU_utilization = round(100 * useful_time / (elapsedTime + 1), 3)
   
    f = open(filename, "a")
    f.write('Algorithm SJF\n')
    f.write(f'-- average CPU burst time: {"%.3f" % round(average_cpu_burst_time, 3)} ms\n')
    f.write(f'-- average wait time: {"%.3f" % round(average_wait_time, 3)} ms\n')
    f.write(f'-- average turnaround time: {"%.3f" % round(average_turnaround_time, 3)} ms\n')
    f.write(f'-- total number of context switches: {context_switches}\n')
    f.write(f'-- total number of preemptions: 0\n')
    f.write(f'-- CPU utilization: {"%.3f" % CPU_utilization}%\n')
    f.close()    