import process
import math 

' SHORTEST JOB FIRST '

def sjf(processes, file):
    queue = []
    io_proccess = []
    terminated = []
    running = []
    processes.sort(key = lambda x : x.numCPUBursts)
    count = 0
    current_queue = []
    elapsedTime = 0
    print("time 0ms: Simulator started for SJF [Q: empty]")
    while True:
        if (elapsedTime == processes[count].arrival):
            queue.append(processes[count])
            current_queue.append(processes[count].name)
            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue [Q:{}]".format(elapsedTime, processes[count].name, processes[count].tau, processes[count].name))
            elapsedTime+=queue[-1].arrival

        if (len(running)==0 and len(queue)!=0):
            running.append(processes[count])

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