from collections import deque

A, B, C, D, E, F = tuple(range(6))

state = A
tape = deque([0])
p = 0

for _ in range (12861455):
    if p < 0:
        tape.appendleft(0)
        p = 0
    elif p >= len(tape):
        tape.append(0)

    if state == A:
        if tape[p] == 0:
            tape[p] = 1
            p += 1
            state = B
        elif tape[p] == 1:
            tape[p] = 0
            p -= 1
            state = B

    elif state == B:
        if tape[p] == 0:
            tape[p] = 1
            p -= 1
            state = C
        elif tape[p] == 1:
            tape[p] = 0
            p += 1
            state = E

    elif state == C:
        if tape[p] == 0:
            tape[p] = 1
            p += 1
            state = E
        elif tape[p] == 1:
            tape[p] = 0
            p -= 1
            state = D

    elif state == D:
        if tape[p] == 0:
            tape[p] = 1
            p -= 1
            state = A
        elif tape[p] == 1:
            tape[p] = 1
            p -= 1
            state = A

    elif state == E:
        if tape[p] == 0:
            tape[p] = 0
            p += 1
            state = A
        elif tape[p] == 1:
            tape[p] = 0
            p += 1
            state = F

    elif state == F:
        if tape[p] == 0:
            tape[p] = 1
            p += 1
            state = E
        elif tape[p] == 1:
            tape[p] = 1
            p += 1
            state = A


print(sum(tape))
