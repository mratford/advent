from collections import namedtuple
from heapq import heappop, heappush


Point = namedtuple('Point', 'x y')
State = namedtuple('State', 'dist_to_nearest position numbers_left')


def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def add_points(p1, p2):
    return Point(p1.x + p2.x, p1.y + p2.y)

def manhattan_neighbours(p):
    for dx in (-1, 1):
        yield Point(p.x + dx, p.y)
    for dy in (-1, 1):
        yield Point(p.x, p.y + dy)


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

def new_state(p, ns):
    return State(dist_to_nearest(p, ns), p, ns)

def distance(s):
    return len(s.numbers_left)

def dist_to_nearest(p, numbers):
    if numbers:
        return min([manhattan_distance(p, number_locations[n])
                    for n in numbers])
    else:
        return 0

def moves(s):
    for x, y in manhattan_neighbours(s.position):
        c = ducts[y][x]
        if c != '#':
            if c.isdigit():
                yield new_state(Point(x, y), s.numbers_left - {int(c)})
            else:
                yield new_state(Point(x, y), s.numbers_left)


with open('input', 'rt') as f:
    ducts = [l.strip() for l in f]

number_locations = {}
for y, row in enumerate(ducts):
    for x, c in enumerate(row):
        if c.isdigit():
            number_locations[int(c)] = Point(x, y)
numbers = frozenset(number_locations.keys())

initial_state = new_state(number_locations[0], numbers - {0})

result = astar(initial_state, moves, distance)
#print(result)
#print(result[-1])
print(len(result) - 1)
print(number_locations)
