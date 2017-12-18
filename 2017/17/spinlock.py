from collections import deque

def d_run_n(spinlock, step_number, n):
    for i in range(1, n + 1):
        spinlock.rotate(-step_number-1)
        spinlock.appendleft(i)
        
    return spinlock

answer = d_run_n(deque([0]), 335, 50000000)
print(answer[answer.index(0) + 1])
