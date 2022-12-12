from collections import defaultdict
from heapq import heappop, heappush


def climbable(height_from, height_to):
    if height_from == "S":
        height_from = "a"
    elif height_from == "E":
        height_from = "z"
    if height_to == "S":
        height_to = "a"
    elif height_to == "E":
        height_to = "z"

    return ord(height_to) - ord(height_from) <= 1


def parse_data(s):
    heightmap = s.strip().splitlines()

    g = defaultdict(list)

    for r, row in enumerate(heightmap):
        for c, height in enumerate(row):
            if height == "S":
                start_point = (r, c)
            elif height == "E":
                end_point = (r, c)
            for d in (-1, 1):
                if 0 <= r + d < len(heightmap):
                    if climbable(height, heightmap[r + d][c]):
                        g[(r, c)].append((r + d, c))
                if 0 <= c + d < len(row):
                    if climbable(height, heightmap[r][c + d]):
                        g[(r, c)].append((r, c + d))

    return (g, start_point, end_point, heightmap)


def manhattan_distance(point_a, point_b):
    a_r, a_c = point_a
    b_r, b_c = point_b
    return abs(a_r - b_r) + abs(a_c - b_c)


def part_1(g, start_point, end_point):
    "A* search with manhattan distance to end as heuristic"
    seen = set()
    # heapq with manhattan distance heuristic and distance travelled so far
    q = [(manhattan_distance(start_point, end_point), 0, start_point)]

    while True:
        _, distance_so_far, this_point = heappop(q)
        if this_point not in seen:
            seen.add(this_point)
            for next_point in g[this_point]:
                if next_point == end_point:
                    return distance_so_far + 1
                elif next_point not in seen:
                    heappush(
                        q,
                        (
                            distance_so_far
                            + 1
                            + manhattan_distance(next_point, end_point),
                            distance_so_far + 1,
                            next_point,
                        ),
                    )


def part_2(g, end_point, heightmap):
    treks = []
    for r, row in enumerate(heightmap):
        for c, height in enumerate(row):
            if height in ["a", "S"]:
                try:
                    treks.append(part_1(g, (r, c), end_point))
                except:
                    # Presumably some points have no path to the summit
                    pass
    return min(treks)


if __name__ == "__main__":
    g, start_point, end_point, heightmap = parse_data(open("input").read())
    print("Part 1:", part_1(g, start_point, end_point))
    print("Part 2:", part_2(g, end_point, heightmap))
