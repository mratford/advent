from dataclasses import dataclass

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
    

N = Point(0, 1)
S = Point(0, -1)
W = Point(-1, 0)
E = Point(1, 0)

def parse_data(s):
    directions = {
        "|": [N, S],
        "-": [E, W],
        "L": [N, E],
        "J": [N, W],
        "7": [S, W],
        "F": [S, E]
    }
    g = {}
    
    for y, line in enumerate(reversed(s.strip().splitlines())):
        for x, c in enumerate(line):
            p = Point(x, y)
            if c in directions:
                g[p] = {p + d for d in directions[c]}
            elif c == "S":
                starting_point = p
                
    # Find the positions the starting point is connected to
    g[starting_point] = {loc for loc in g if starting_point in g[loc]}
    
    return starting_point, g

def strip_nodes(data):
    starting_point, g = data
    current_location = next(iter(g[starting_point]))
    locations_visited = {starting_point, current_location}
    while (
        next_locations := [
            p  
            for p in g[current_location]
            if p not in locations_visited
        ]):
        current_location = next_locations[0]
        locations_visited.add(current_location)
    for k in list(g.keys()):
        if k not in locations_visited:
            del g[k]
    return g

def double_map(g):
    new_map = set()
    for p in g:
        new_p = p * 2
        new_map.add(new_p)
        for nbr in g[p]:
            d = nbr - p
            new_map.add(new_p + d)
    return new_map

def part_2(data):
    ps = double_map(strip_nodes(data))
    min_x = min(p.x for p in ps)
    max_x = max(p.x for p in ps)
    min_y = min(p.y for p in ps)
    max_y = max(p.y for p in ps)
    
    inner = set()
    outer = set()
    
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (p := Point(x, y)) not in (ps | inner | outer):
                q = [p]
                connected = {p}
                hit_boundary = False
                while q and not hit_boundary:
                    loc = q.pop()
                    for d in (N, S, E, W):
                        if (nbr := loc + d) not in (ps | connected):
                            if (
                                nbr.x < min_x 
                                or nbr.x > max_x 
                                or nbr.y < min_y
                                or nbr.y > max_y
                            ):
                                hit_boundary = True
                            else:
                                q.append(nbr)
                                connected.add(nbr)
                if not hit_boundary:
                    inner = inner | connected
                else:
                    outer = outer | connected

    even_ps = [
        p 
        for p in inner 
        if p.x % 2 == 0 and p.y % 2 == 0
    ]
        
    lines = []
    min_x = min(p.x for p in ps)
    max_x = max(p.x for p in ps)
    min_y = min(p.y for p in ps)
    max_y = max(p.y for p in ps)
    for y in range(max_y, min_y - 1, -1):
        lines.append(
            "".join(
                "I" if Point(x, y) in even_ps else
                "#" if Point(x, y) in ps else "."
                for x in range(min_x, max_x + 1)
            )
        )

    return len(even_ps)

data = parse_data(open("input").read())

print(part_2(data))