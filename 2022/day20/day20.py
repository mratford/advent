from dataclasses import dataclass


@dataclass
class TwoWayPointer:
    prev: int
    next: int


def parse_data(s):
    return [int(x) for x in s.strip().splitlines()]


def part_1(data):
    # Represent the data as a circular loop where each index into the data
    # has a pointer to the previous and next indices in the data. Manipulate
    # these pointers, which is cheap, rather than the actual data, which
    # is expensive.

    circular = {}
    n = len(data)

    for i, x in enumerate(data):
        if x == 0:
            zero_loc = i
        circular[i] = TwoWayPointer((i - 1) % n, (i + 1) % n)

    for i in range(n):
        next_loc = i
        steps = data[i] % (n - 1)
        if steps != 0:
            # n - 1 as the datum is moved out of the list
            for _ in range(steps):
                next_loc = circular[next_loc].next
            # Remove current link
            circular[circular[i].prev].next = circular[i].next
            circular[circular[i].next].prev = circular[i].prev
            # Add new link
            old_next = circular[next_loc].next
            circular[next_loc].next = i
            circular[old_next].prev = i
            circular[i].prev = next_loc
            circular[i].next = old_next

        debug = []
        loc = zero_loc
        for _ in range(n):
            debug.append(data[loc])
            loc = circular[loc].next

    loc = zero_loc
    grove_coords = []
    for i in range(3):
        for _ in range(1000):
            loc = circular[loc].next
        grove_coords.append(data[loc])

    return sum(grove_coords)


def part_2(data):
    # Represent the data as a circular loop where each index into the data
    # has a pointer to the previous and next indices in the data. Manipulate
    # these pointers, which is cheap, rather than the actual data, which
    # is expensive.

    data = [811589153 * x for x in data]
    circular = {}
    n = len(data)

    for i, x in enumerate(data):
        if x == 0:
            zero_loc = i
        circular[i] = TwoWayPointer((i - 1) % n, (i + 1) % n)

    for _ in range(10):
        for i in range(n):
            next_loc = i
            steps = data[i] % (n - 1)
            if steps != 0:
                # n - 1 as the datum is moved out of the list
                for _ in range(steps):
                    next_loc = circular[next_loc].next
                # Remove current link
                circular[circular[i].prev].next = circular[i].next
                circular[circular[i].next].prev = circular[i].prev
                # Add new link
                old_next = circular[next_loc].next
                circular[next_loc].next = i
                circular[old_next].prev = i
                circular[i].prev = next_loc
                circular[i].next = old_next

    loc = zero_loc
    grove_coords = []
    for i in range(3):
        for _ in range(1000):
            loc = circular[loc].next
        grove_coords.append(data[loc])

    return sum(grove_coords)


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))
