from dataclasses import dataclass
import heapq
import math

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

N = Point(0, 1)
S = Point(0, -1)
W = Point(-1, 0)
E = Point(1, 0)

DIRECTIONS = {N, E, S, W}

def manhattan(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def parse_data(s):
    grid = {}
    lines = s.strip().splitlines()
    starting_point = None
    end_point = None
    for y, line in zip(range(len(lines) - 1, -1, -1), lines):
        for x, c in enumerate(line):
            grid[Point(x, y)] = c
            if c == "S":
                starting_point = Point(x, y)
            elif c == "E":
                end_point = Point(x, y)
    return grid, starting_point, end_point

def shortest_path(grid, starting_point, end_point):
    q = [(manhattan(starting_point, end_point), 0, starting_point)]
    seen = {}

    while q:
        _, length, p = heapq.heappop(q)
        for d in DIRECTIONS:
            n = p + d
            if n == end_point:
                return length + 1
            if grid[n] == "." and seen.get(n, math.inf) > length + 1:
                seen[n] = length + 1
                heapq.heappush(q, (length + 1 + manhattan(n, end_point), length + 1, n))

def part_1(data, save_value=100):
    grid, starting_point, end_point = data
    target = shortest_path(grid, starting_point, end_point) - save_value
    q = [(0, starting_point, None, set())]
    cheats = set()
    result = 0
    
    while q:
        length, p, cheat, path_so_far = q.pop()
        if p == end_point and length <= target:
            cheats.add(cheat)
            result += 1
        else:
            for d in DIRECTIONS:
                n = p + d
                if n in grid:
                    l = length + 1
                    h = l + manhattan(n, end_point)
                    if h <= target and n not in path_so_far:
                        if grid[n] in (".", "E") and cheat not in cheats:
                            q.append((l, n, cheat, path_so_far | {n}))
                        elif grid[n] == "#" and cheat is None and n not in cheats:
                            q.append((l, n, n, path_so_far | {n}))

    return len(cheats), result

def part_1(data, save_value=100):
    grid, starting_point, end_point = data
    target = shortest_path(grid, starting_point, end_point) - save_value
    q = [(0, starting_point, None, set())]
    cheats = set()
    result = 0
    
    while q:
        length, p, cheat, path_so_far = q.pop()
        if p == end_point and length <= target:
            cheats.add(cheat)
            result += 1
        else:
            for d in DIRECTIONS:
                n = p + d
                if n in grid:
                    l = length + 1
                    h = l + manhattan(n, end_point)
                    if h <= target and n not in path_so_far:
                        if grid[n] in (".", "E") and cheat not in cheats:
                            q.append((l, n, cheat, path_so_far | {n}))
                        elif grid[n] == "#" and cheat is None and n not in cheats:
                            q.append((l, n, n, path_so_far | {n}))

    return len(cheats), result

if __name__ == "__main__":
    data = parse_data(open("input").read())
    print(part_1(data))
