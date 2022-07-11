' SHORTEST JOB FIRST '
'''
pid   CPU burst times
   P1      18 ms
   P2       3 ms
   P3       4 ms

  ready queue is ordered: P2 P3 P1    (priority queue)

 (assume that all processes arrive in the ready queue at time 0)

    context switches           context switch
       v   v    v                  v
       +---+----+------------------+------------------->
  SJF: |P2 | P3 | P1               | .................
       +---+----+------------------+------------------->
    t: 0   3    7                  25


  P1 has 7 ms wait time      P1 has 25 ms turnaround time
  P2 has 0 wait time         P2 has 3 ms turnaround time
  P3 has 3 ms wait time      P3 has 7 ms turnaround time
'''


def sjf(processlist, simout):
    '''
    
    '''


if __name__ == "__main__":
    print()