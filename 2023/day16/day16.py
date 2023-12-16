from dataclasses import dataclass
from collections import namedtuple
from multiprocessing import Pool


Beam = namedtuple("Beam", "loc direction")


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

    def __mul__(self, multiple):
        return self.__class__(self.x * multiple, self.y * multiple)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


N = Point(0, 1)
S = Point(0, -1)
W = Point(-1, 0)
E = Point(1, 0)

beam_redirects = {
    "|": {N: [N], S: [S], W: [N, S], E: [N, S]},
    "-": {N: [E, W], S: [E, W], W: [W], E: [E]},
    "/": {
        N: [E],
        S: [W],
        W: [S],
        E: [N],
    },
    "\\": {N: [W], S: [E], W: [N], E: [S]},
    ".": {x: [x] for x in [N, S, E, W]},
}


def parse_data(s):
    grid = {}
    lines = s.strip().splitlines()
    for y, line in zip(range(len(lines) - 1, -1, -1), lines):
        for x, c in enumerate(line):
            grid[Point(x, y)] = c
    return grid


def n_energised_parallel(data):
    grid, starting_beam = data
    beams = [starting_beam]
    energised = set()
    seen_states = set()

    while beams:
        beam = beams.pop()
        if beam not in seen_states:
            seen_states.add(beam)
            new_loc = beam.loc + beam.direction
            if new_loc in grid:
                energised.add(new_loc)
                for new_direction in beam_redirects[grid[new_loc]][beam.direction]:
                    beams.append(Beam(new_loc, new_direction))

    return len(energised)


def all_energised_parallel(grid):
    max_x = max(p.x for p in grid)
    max_y = max(p.y for p in grid)
    beams = []
    for x in range(0, max_x + 1):
        beams.append(Beam(Point(x, -1), N))
        beams.append(Beam(Point(x, max_y + 1), S))
    for y in range(0, max_y + 1):
        beams.append(Beam(Point(-1, y), E))
        beams.append(Beam(Point(max_x + 1, y), W))
    with Pool() as p:
        return p.map(n_energised_parallel, [(grid, beam) for beam in beams])


def part_2_parallel(grid):
    return max(all_energised_parallel(grid))


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print(part_2_parallel(data))
