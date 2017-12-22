from collections import namedtuple
from pyrsistent import pdeque, pset


State = namedtuple('State', 'weakened infected flagged virus_p virus_d total_infections')


def initialise(data):
    def up(p): return (p[0]-1, p[1])
    def right(p): return (p[0], p[1]+1)
    def down(p): return (p[0]+1, p[1])
    def left(p): return (p[0], p[1]-1)

    weakened = pset()
    infected = pset({(r, c) 
                     for r, row in enumerate(data) 
                     for c, ch in enumerate(row) 
                     if ch == '#'})
    flagged = pset()
    
    virus_position = (len(data) // 2, len(data[0]) // 2)
    virus_direction = pdeque([up, right, down, left])
    
    return State(weakened, infected, flagged, virus_position, virus_direction, 0)


def move(state):
    weakened, infected, flagged, v_p, v_d, infections = state
    
    if v_p in infected:
        # turn right
        v_d = v_d.rotate(-1)
        # flag
        infected = infected.remove(v_p)
        flagged = flagged.add(v_p)
    elif v_p in weakened:
        # infect
        weakened = weakened.remove(v_p)
        infected = infected.add(v_p)
        infections = infections + 1
    elif v_p in flagged:
        # turn around
        v_d = v_d.rotate(2)
        # clean
        flagged = flagged.remove(v_p)
    else: # clean
        # turn left
        v_d = v_d.rotate(1)
        # weaken
        weakened = weakened.add(v_p)
        
    
    # move - left is the leftmost i.e. current direction
    v_p = v_d.left(v_p)
    
    return State(weakened, infected, flagged, v_p, v_d, infections)


def run_n(data, n):
    s = initialise(data)
    
    for _ in range(n):
        s = move(s)
        
    return s

with open('input', 'r') as f:
    problem_data = open('input', 'r').read().strip().splitlines()

print(run_n(problem_data, 10000000).total_infections)
