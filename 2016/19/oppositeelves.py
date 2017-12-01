from collections import deque
from math import floor


num_elves = 3018458


def last_elf(no_of_elves):
    elves = deque(range(1, num_elves + 1))
    elves.rotate(-floor(num_elves/2))
    odd = num_elves % 2 != 0

    while len(elves) > 1:
        elves.popleft()
        if odd:
            elves.rotate(-1)
        odd = not odd
    return elves.pop()


print(last_elf(num_elves))
