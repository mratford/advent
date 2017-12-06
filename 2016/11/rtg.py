from collections import namedtuple
from heapq import heappush, heappop
import sys
from itertools import chain, combinations
import math

Facility = namedtuple("Facility", "level floors")
Candidate = namedtuple('Candidate', 'min_steps, steps_so_far, facility')
floors = {0, 1, 2, 3}


def min_steps_to_solution(facility):
    return math.ceil(sum([len(facility.floors[f]) * (3 - f) for f in [0, 1, 2]])/2)


def is_valid(facility):
    for f in floors:
        gens = [y[0] for y in facility.floors[f] if y[1] == 'g']
        chips = [y[0] for y in facility.floors[f] if y[1] == 'm']
        for chip in chips:
            if gens and chip not in gens:
                return False
    return True


def move_items(facility, new_level, items):
    new_floors = []
    for i in range(4):
        if i == new_level:
            new_floors.append(facility.floors[i] | items)
        elif i == facility.level:
            new_floors.append(facility.floors[i] - items)
        else:
            new_floors.append(facility.floors[i])
    return Facility(new_level, tuple(new_floors))


def indexed_facility(facility):
    indexed_floors = []
    index = {}
    i = 0
    for f in facility.floors:
        indexed_floors.append([])
        for elem, type in f:
            if elem not in index:
                index[elem] = i
                i += 1
            indexed_floors[-1].append((index[elem], type))
    return Facility(facility.level, tuple([frozenset(f) for f in indexed_floors]))

start = 'pr,g pr,m:co,g cu,g ru,g pl,g:co,m cu,m ru,m pl,m:'
# start = 'pr,g pr,m e,g e,m d,g d,m:co,g cu,g ru,g pl,g:co,m cu,m ru,m pl,m:'
starting_facility = Facility(0, tuple([frozenset([tuple(x.split(','))
                                                  for x in f.split(' ') if x])
                                       for f in start.split(':')]))

# starting_facility == Facility(0, (frozenset({('pr', 'g'), ('pr, 'm')}),
#                                   frozenset... 

seen = {indexed_facility(starting_facility): 0}
candidates = [Candidate(min_steps_to_solution(starting_facility), 0, starting_facility)]

while candidates:
    c = heappop(candidates)
    level = c.facility.level
    items_on_floor = c.facility.floors[level]
    steps_so_far = c.steps_so_far
    for items_to_move in chain(combinations(items_on_floor, 1),
                               combinations(items_on_floor, 2)):
        for new_level in {level - 1, level + 1} & floors:
            new_facility = indexed_facility(move_items(c.facility, new_level, set(items_to_move)))
            if is_valid(new_facility):
                steps_to_go = min_steps_to_solution(new_facility)
                if steps_to_go == 0:
                    print('Solution', steps_so_far + 1)
                    sys.exit()
                elif new_facility not in seen or seen[new_facility] > steps_so_far + 1:
                    heappush(candidates, Candidate(steps_to_go + steps_so_far + 1,
                                                   steps_so_far + 1, new_facility))
                    seen[new_facility] = steps_so_far + 1

print('No solution found')

