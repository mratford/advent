from itertools import count


def parse_data(s):
    l = []
    for pair in s.strip().split("\n\n"):
        l.append(tuple(eval(p) for p in pair.split("\n")))
    return l


def right_order(left, right):
    pass


def part_1(data):
    return sum(i if right_order(*p) else 0 for i, p in zip(count(1), data))


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print("Part 1:", part_1(data))
