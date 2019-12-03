import itertools


# Generator yielding coordinates for a specified wire
def wire_path(wire_spec):
    x, y = (0, 0)

    for command in wire_spec.strip().split(','):
        direction = command[0]
        steps = int(command[1:])

        dx, dy = (0, 0)

        if direction == 'R': 
            dx = 1
        elif direction == 'L':
            dx = -1
        elif direction == 'U':
            dy = 1
        elif direction == 'D':
            dy = -1

        for _ in range(steps):
            yield (x := x + dx, y := y + dy)


def solve_part_1(wire_spec_1, wire_spec_2):
    # Intersections are the points covered by both wires
    intersections: Set[Tuple[int, int]] = (set(wire_path(wire_spec_1)) 
                                           & set(wire_path(wire_spec_2)))
    return sum(min(intersections, key=lambda p: abs(p[0]) + abs(p[1])))


def time_to_point(wire_spec):
    time_dict = {}
    
    for p, t in zip(wire_path(wire_spec), itertools.count(start=1)):
        # Only want to record the first time the coordinate is reached
        if p not in time_dict:
            time_dict[p] = t
            
    return time_dict


def solve_part_2(wire_spec_1, wire_spec_2):
    times_1 = time_to_point(wire_spec_1)
    times_2 = time_to_point(wire_spec_2)
    
    intersections = set(times_1) & set(times_2)
    intersection_times = {p: times_1[p] + times_2[p] for p in intersections}
    return min(intersection_times.values())


if __name__ == '__main__':
    f = open('input', 'r')
    wire_spec_1 = f.readline()
    wire_spec_2 = f.readline()
    print(f'Part 1: {solve_part_1(wire_spec_1, wire_spec_2)}')
    print(f'Part 2: {solve_part_2(wire_spec_1, wire_spec_2)}')