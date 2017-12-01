import re
from collections import namedtuple
import copy
from heapq import heappop, heappush


def astar(start_state, move_function, distance_function):
    states = [(distance_function(start_state), start_state)]
    paths = {start_state: None}
    path_lengths = {start_state: 0}
    while states:
        print (len(states), len(paths))
        _, best = heappop(states)
        for s in move_function(best):
            d = distance_function(s)
            pl = path_lengths[best] + 1
            if s not in path_lengths or path_lengths[s] > pl:
                path_lengths[s] = pl
                paths[s] = best
                heappush(states, (d + pl, s))
                if d == 0:
                    return get_path(paths, s)
    return paths

def get_path(paths, state):
    if state is None:
        return []
    else:
        return get_path(paths, paths[state]) + [state]
    
Node = namedtuple('Node', 'size used avail')
node_re = re.compile(r'/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T'
                     r'\s+(?P<used>\d+)T\s+(?P<avail>\d+)T')
nodes = {}

with open('input', 'rt') as f:
    for line in f:
        m = node_re.match(line)
        if m:
            nodes[(int(m.group(1)), int(m.group(2)))] = \
              Node(*[int(x) for x in m.group(3, 4, 5)])

empty_node = [n for n in nodes if nodes[n].used == 0][0]
goal_x, goal_y = 0, 0

for y in range(30):
    s = ''
    for x in range(33):
        if (x, y) == (goal_x, goal_y):
            s += 'g'
        elif (x, y) == empty_node:
            s+= 'e'
        elif (x, y) == (0, 0):
            s += 'd'
        elif nodes[(x,y)].size >= 500:
            s += '*'
        else:
            s += '.'
    print(s)
    
# Hacks for this particular data set from this point onwards
nodes = {k: v for (k, v) in nodes.items() if v.size < 500}

initial_state = (empty_node, (max([x for x, _ in nodes]), 0))

def distance(state):
    x, y = state[1]
    return abs(goal_x - x) + abs(goal_y - y)

def moves(state):
    valid_moves = []
    empx, empy = state[0]
    data_pos = state[1]
    for n in [(empx - 1, empy), (empx + 1, empy), (empx, empy - 1),
              (empx, empy +  1)]:
        if n in nodes and nodes[n].used <= nodes[(empx, empy)].size:
            if n == data_pos:
                valid_moves.append((n, (empx, empy)))
            else:
                valid_moves.append((n, data_pos))
    return valid_moves
                
paths = astar(initial_state, moves, distance)
print(len(paths) - 1)
