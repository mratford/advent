import functools
from heapq import heappop, heappush
from collections import namedtuple
import sys


fav_number = 1352
destination = (31, 39)


Path = namedtuple('Path', 'min_steps steps_so_far coords')

@functools.lru_cache(maxsize=None)
def is_open(coords):
    x, y = coords
    bits = [int(b) for b in bin(x*x + 3*x + 2*x*y + y + y*y + fav_number)[2:]]
    return sum(bits) % 2 == 0
    
def distance(coords):
    x, y = coords
    dx, dy = destination
    return abs(dx - x) + abs(dy - y)

start = (1, 1)
been = {start: 0}
paths = [Path(distance(start), 0, start)]

while paths:
    print(paths[0])
    _, steps_so_far, coords = heappop(paths)
    for i in (0, 1):
        for step in (-1, 1):
            new_pos = list(coords)
            new_pos[i] += step
            new_pos = tuple(new_pos)
            if is_open(new_pos):
                h = distance(new_pos)
                steps_taken = steps_so_far + 1
                if h == 0:
                    print(steps_taken)
                    sys.exit()
                if new_pos[i] >= 0:
                    if new_pos not in been or been[new_pos] > steps_taken:
                        been[new_pos] = steps_taken
                        heappush(paths, Path(h + steps_taken, steps_taken,
                                             new_pos))

print("No path found")
                             
