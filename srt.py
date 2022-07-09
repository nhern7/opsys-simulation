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

def srt():
    '''
    
    '''


if __name__ == "__main__":
    print()