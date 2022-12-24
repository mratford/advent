from dataclasses import dataclass
from functools import cache
from copy import deepcopy
from heapq import heappop, heappush
from collections import Counter


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        else:
            return self.y < other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __mod__(self, other):
        if isinstance(other, Point):
            return self.__class__(self.x % other.x, self.y % other.y)
        else:
            return self.__class__(self.x % other, self.y % other)


def parse_data(s):
    dirs = {"<": Point(-1, 0), "^": Point(0, 1), ">": Point(1, 0), "v": Point(0, -1)}
    lines = list(reversed(s.strip().splitlines()[1:-1]))
    bound = Point(len(lines[0]) - 2, len(lines))
    blizzards = {}
    for y, line in enumerate(lines):
        line = line.strip("#")
        for x, c in enumerate(line):
            if c != ".":
                blizzards[Point(x, y)] = dirs[c]
    # return blizzards and bounding point
    return (blizzards, bound)


def new_blizzards(blizzards, bound):
    newb = []
    for b, d in blizzards:
        newb.append(((b + d) % bound, d))
    return newb


def blizzards_over_time(blizzards, bound):
    # Need to represent the blizzards as a list as otherwise they merge.
    # Return to the search function as a set.
    original_blizzards = deepcopy(blizzards)

    blizzard_list = [(k, v) for k, v in original_blizzards.items()]

    @cache
    def blizzard_lists_after(time):
        if time == 0:
            return blizzard_list
        elif time == 1:
            return new_blizzards(blizzard_list, bound)
        else:
            return new_blizzards(blizzard_lists_after(time - 1), bound)

    @cache
    def blizzards_after(time):
        return {p for p, _ in blizzard_lists_after(time)}

    return blizzards_after


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def part_1(blizzards, bound):
    # A* search with manhattan distance to end as heuristic

    blizzards_after_time = blizzards_over_time(blizzards, bound)
    start = Point(0, bound.y)
    goal = Point(bound.x - 1, -1)
    seen = set()
    # heapq with manhattan distance heuristic and minutes so far
    q = [(manhattan(start, goal), 0, start)]

    while True:
        h, minutes_so_far, this_point = heappop(q)
        if (this_point, minutes_so_far) not in seen:
            seen.add((this_point, minutes_so_far))
            next_blizzards = blizzards_after_time(minutes_so_far + 1)

            for next_point in [
                this_point + Point(*d) for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            ]:
                if next_point == goal:
                    return minutes_so_far + 1
                elif (
                    (next_point, minutes_so_far + 1) not in seen
                    and next_point not in next_blizzards
                    and 0 <= next_point.x < bound.x
                    and 0 <= next_point.y < bound.y
                ):
                    heappush(
                        q,
                        (
                            minutes_so_far + 1 + manhattan(next_point, goal),
                            minutes_so_far + 1,
                            next_point,
                        ),
                    )
            # Wait for blizzards to clear
            if this_point not in next_blizzards:
                heappush(q, (h + 1, minutes_so_far + 1, this_point))


def blizzard_search(bound, start, goal, time, blizzards_after_time):
    seen = set()
    # heapq with manhattan distance heuristic and minutes so far
    q = [(time + manhattan(start, goal), time, start)]

    while True:
        h, minutes_so_far, this_point = heappop(q)
        if (this_point, minutes_so_far) not in seen:
            seen.add((this_point, minutes_so_far))
            next_blizzards = blizzards_after_time(minutes_so_far + 1)

            for next_point in [
                this_point + Point(*d) for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            ]:
                if next_point == goal:
                    return minutes_so_far + 1
                elif (
                    (next_point, minutes_so_far + 1) not in seen
                    and next_point not in next_blizzards
                    and 0 <= next_point.x < bound.x
                    and 0 <= next_point.y < bound.y
                ):
                    heappush(
                        q,
                        (
                            minutes_so_far + 1 + manhattan(next_point, goal),
                            minutes_so_far + 1,
                            next_point,
                        ),
                    )
            # Wait for blizzards to clear
            if this_point not in next_blizzards:
                heappush(q, (h + 1, minutes_so_far + 1, this_point))


def part_2(blizzards, bound):
    blizzards_after_time = blizzards_over_time(blizzards, bound)
    start = Point(0, bound.y)
    goal = Point(bound.x - 1, -1)
    t1 = blizzard_search(bound, start, goal, 0, blizzards_after_time)
    t2 = blizzard_search(bound, goal, start, t1, blizzards_after_time)
    return blizzard_search(bound, start, goal, t2, blizzards_after_time)


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print("Part 1: ", part_1(*data))
    print("Part 2: ", part_2(*data))
