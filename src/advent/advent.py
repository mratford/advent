from dataclasses import dataclass
from functools import cache, partial

@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

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

@cache
def north():
    return Point(0, 1)

@cache
def south(): 
    return Point(0, -1)

@cache
def west():
    return Point(-1, 0)

@cache
def east():
    return Point(1, 0)

@cache
def directions(diagonals = False):
    if not diagonals:
        return [north(), east(), south(), west()]
    else:
        return [
            north(), 
            north() + east(),
            east(),
            south() + east(),
            south(),
            south() + west(),
            west(),
            north() + west()
        ]
        
all_directions = partial(directions, diagonals=True)

def manhattan(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def parse_grid(s):
    grid = {}
    lines = s.strip().splitlines()
    starting_point = None
    end_point = None
    for y, line in zip(range(len(lines) - 1, -1, -1), lines):
        for x, c in enumerate(line):
            grid[Point(x, y)] = c
    return grid

def read_input():
    return open("input").read()