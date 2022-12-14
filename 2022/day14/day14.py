from copy import deepcopy


def parse_data(s):
    g = {}
    for line in s.strip().splitlines():
        coords = [tuple(map(int, c.split(","))) for c in line.split(" -> ")]
        for (x1, y1), (x2, y2) in zip(coords, coords[1:]):
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    g[(x1, y)] = "#"
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    g[(x, y1)] = "#"
    return g


def draw_cavern(g):
    xs = [x for x, _ in g]
    ys = [y for _, y in g]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    for y in range(min_y, max_y + 1):
        print("".join(g.get((x, y), ".") for x in range(min_x, max_x + 1)))


def add_sand(g, last_row):
    x, y = 500, 0
    # hack
    if g.get((500, 0), "") == "o":
        return False
    while y <= last_row:
        while (x, y + 1) not in g and y <= last_row:
            y += 1
        if (x - 1, y + 1) not in g:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in g:
            x += 1
            y += 1
        else:
            g[(x, y)] = "o"
            return g
    return False


def part_1(g):
    g = deepcopy(g)
    grains = 0
    last_row = max(y for _, y in g)
    # draw_cavern(g)
    while g := add_sand(g, last_row):
        # draw_cavern(g)
        grains += 1
    return grains


def part_2(g):
    g = deepcopy(g)
    floor = max(y for _, y in g) + 2
    # hack, hack, hack
    for x in range(500 - floor - 1000, 500 + floor + 1000):
        g[(x, floor)] = "#"
    return part_1(g)


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))
