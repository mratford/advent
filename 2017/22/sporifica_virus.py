from collections import namedtuple, deque


State = namedtuple('State', 'weakened infected flagged virus_p virus_d total_infections')


def initialise(data):
    def up(p): return (p[0]-1, p[1])
    def right(p): return (p[0], p[1]+1)
    def down(p): return (p[0]+1, p[1])
    def left(p): return (p[0], p[1]-1)

    weakened = set()
    infected = set({(r, c) 
                    for r, row in enumerate(data) 
                    for c, ch in enumerate(row) 
                    if ch == '#'})
    flagged = set()
    
    virus_position = (len(data) // 2, len(data[0]) // 2)
    virus_direction = deque([up, right, down, left])
    
    return State(weakened, infected, flagged, virus_position, virus_direction, 0)


def move(state):
    weakened, infected, flagged, v_p, v_d, infections = state
    
    if v_p in infected:
        # turn right
        v_d.rotate(-1)
        # flag
        infected.remove(v_p)
        flagged.add(v_p)
    elif v_p in weakened:
        # infect
        weakened.remove(v_p)
        infected.add(v_p)
        infections += 1
    elif v_p in flagged:
        # turn around
        v_d.rotate(2)
        # clean
        flagged.remove(v_p)
    else: # clean
        # turn left
        v_d.rotate(1)
        # weaken
        weakened.add(v_p)
        
    v_p = v_d[0](v_p)
    
    return State(weakened, infected, flagged, v_p, v_d, infections)


def run_n(data, n):
    s = initialise(data)
    
    for _ in range(n):
        s = move(s)
        
    return s


with open('input', 'r') as f:
    problem_data = open('input', 'r').read().strip().splitlines()

print(run_n(problem_data, 10000000).total_infections)
