from dataclasses import dataclass
from collections import deque, Counter
from itertools import count


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

    def __iter__(self):
        yield self.x
        yield self.y


W = Point(-1, 0)
NW = Point(-1, 1)
N = Point(0, 1)
NE = Point(1, 1)
E = Point(1, 0)
SE = Point(1, -1)
S = Point(0, -1)
SW = Point(-1, -1)


def directions_to_check():
    d = deque([(N, (N, NW, NE)), (S, (S, SW, SE)), (W, (W, NW, SW)), (E, (E, NE, SE))])
    while True:
        yield list(d)
        d.append(d.popleft())


def parse_data(s):
    elves = set()
    for y, row in enumerate(reversed(s.strip().splitlines())):
        for x, c in enumerate(row):
            if c == "#":
                elves.add(Point(x, y))
    return elves


def need_to_move(elf, elves):
    return any(elf + d in elves for d in [N, NE, E, SE, S, SW, W, NW])


def find_move(elf, directions, elves):
    # print()
    # print(f"{elf = }")
    if not need_to_move(elf, elves):
        return elf
    for move, checks in directions:
        # print(f"{move = }")
        # for ch in checks:
        #     print(f"{elf + ch =}")
        #     print(f"{(elf + ch) in elves = }")
        if not any((elf + ch) in elves for ch in checks):
            return elf + move
    return elf


def print_elves(elves):
    xs, ys = tuple(zip(*elves))
    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)

    for y in reversed(range(min_y, max_y + 1)):
        print(
            "".join(
                ["#" if Point(x, y) in elves else "." for x in range(min_x, max_x + 1)]
            )
        )


def part_1(data):
    elves = data
    directions = directions_to_check()

    for _ in range(10):
        ds = next(directions)
        old_elves = list(elves)
        new_elves = [find_move(elf, ds, elves) for elf in elves]
        counts = Counter(new_elves)
        elves = {
            new_elves[i] if counts[new_elves[i]] == 1 else old_elves[i]
            for i in range(len(elves))
        }
        # print_elves(elves)
        # print()

    xs, ys = tuple(zip(*elves))
    return (max(xs) + 1 - min(xs)) * (max(ys) + 1 - min(ys)) - len(elves)


def part_2(data):
    elves = data
    directions = directions_to_check()

    for i in count(1):
        if all(not need_to_move(elf, elves) for elf in elves):
            return i
        ds = next(directions)
        old_elves = list(elves)
        new_elves = [find_move(elf, ds, elves) for elf in elves]
        counts = Counter(new_elves)
        elves = {
            new_elves[i] if counts[new_elves[i]] == 1 else old_elves[i]
            for i in range(len(elves))
        }
        # print_elves(elves)
        # print()


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))
