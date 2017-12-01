import hashlib
from heapq import heappop, heappush


passcode = 'udskfozm'


def astar(start_state, move_function, distance_function):
    states = [(distance_function(start_state), start_state)]
    paths = {start_state: None}
    path_lengths = {start_state: 0}
    while states:
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
            

directions = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
valid_coords = {0, 1, 2, 3}


def unlocked_doors(path):
    h = hashlib.md5((passcode + path).encode('utf-8')).hexdigest()
    return [d for i, d in enumerate('UDLR') if h[i] in 'bcdef']


def valid_moves(state):
    result = []
    (x, y), path = state
    for d in unlocked_doors(path):
        dx, dy = directions[d]
        new_x, new_y = x + dx, y + dy
        if new_x in valid_coords and new_y in valid_coords:
            result.append(((new_x, new_y), path + d))
    return result

def distance(state):
    (x, y), _ = state
    return (3 - x) + (3 - y)

start_state = ((0, 0), '')
result = astar(start_state, valid_moves, distance)
if result:
    print(result[-1][1])
