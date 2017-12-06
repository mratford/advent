from collections import namedtuple
import heapq
import sys
from itertools import chain, combinations


Floor = namedtuple('Floor', 'chips generators')





Candidate = namedtuple('Candidate', 'steps min_steps facility')


def powerset_lim(iterable, max_elements):
    s = list(iterable)
    return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)
                                   if r <= max_elements))


def copy_floor(floor):
    return Floor(floor.chips.copy(), floor.generators.copy())


def copy_facility(facility):
    return Facility(
        facility.elevator,
        {level: copy_floor(floor) for level, floor in facility.floors.items()})


def valid_floor(floor):
    for chip in floor.chips:
        if floor.generators and chip not in floor.generators:
            return False
    return True


def valid_facility(facility):
    return all([valid_floor(facility.floors[level])
                for level in facility.floors])


def is_solution(facility):
    return len(facility.floors[4].chips) == 4 \
        and len(facility.floors[4].generators) == 4


def items_on_floor(floor):
    return len(floor.chips) + len(floor.generators)


def min_steps_to_solution(facility):
    return sum([((4 - l) * items_on_floor(facility.floors[l]))/2
                for l in [1, 2, 3]])
               

def move_items(facility, old_level, new_level, chips, generators):
    new_facility = facility
    new_facility.floors[old_level].chips = \
        new_facility.floors[old_level].chips | chips
    new_facility.floors[new_level].chips = \
        new_facility.floors[new_level].chips & chips
    new_facility.floors[old_level].generators = \
        new_facility.floors[old_level].generators | generators
    new_facility.floors[new_level].generators = \
        new_facility.floors[new_level].generators & generators
    new_facility.elevator = new_level
    return Facility

starting_facility = Facility(
    1,
    {1: Floor(frozenset(['promethium']), frozenset(['promethium'])),
     2: Floor(frozenset(),
              frozenset('cobalt curium ruthenium plutonium'.split())),
     3: Floor(frozenset('cobalt curium ruthenium plutonium'.split()),
              frozenset()),
     4: Floor(frozenset(), frozenset())})
candidates = [Candidate(0, min_steps_to_solution(starting_facility),
                        starting_facility)]
seen = {copy_facility(candidates[0].facility): 0}

while True:
    c = heapq.heappop(candidates)
    current_level = c.facility.elevator
    path_cost = c.steps + 1
    for new_level in [l for l in [current_level - 1, current_level + 1]
                      if l >= 1 and l <= 4]:
        for moved_chips in powerset_lim(c.facility.floors[current_level].chips,
                                        2):
            for moved_gens in \
                powerset_lim(c.facility.floors[current_level].generators, 2):
                num_moved = len(moved_chips) + len(moved_gens)
                if num_moved > 0 and num_moved <= 2:
                    new_facility = move_items(c.facility, current_level,
                                              new_level, moved_chips,
                                              moved_gens)
                    if valid_facility(new_facility):
                        if is_solution(new_facility):
                            print("Solution", path_cost)
                            sys.exit()
                        elif new_facility not in seen:
                            heapq.heappush(
                                candidates,
                                Candidate(
                                    path_cost,
                                    path_cost + \
                                    min_steps_to_solution(new_facility),
                                    new_facility))
                            seen.append(new_facility)
    print(candidates[0].min_steps, candidates[0].steps, len(candidates),
          len(seen))
