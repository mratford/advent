from collections import deque


num_elves = 3018458

def last_elf(no_of_elves):
    elves = deque(range(1, num_elves + 1))

    while len(elves) > 1:
        elves.append(elves.popleft())
        _ = elves.popleft()
    return elves.pop()

print(last_elf(num_elves))
