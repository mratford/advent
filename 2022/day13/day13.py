from itertools import count, chain
from enum import Enum

InOrder = Enum("InOrder", ["FALSE", "UNDECIDED", "TRUE"])


def parse_data(s):
    l = []
    for pair in s.strip().split("\n\n"):
        l.append(tuple(eval(p) for p in pair.split("\n")))
    return l


def right_order(left, right):
    match left, right:
        case int(), list():
            return right_order([left], right)
        case list(), int():
            return right_order(left, [right])
        case int(), int():
            return (
                InOrder.FALSE
                if left > right
                else InOrder.UNDECIDED
                if left == right
                else InOrder.TRUE
            )
        case list(), list():
            for l, r in zip(left, right):
                match right_order(l, r):
                    case InOrder.FALSE:
                        return InOrder.FALSE
                    case InOrder.TRUE:
                        return InOrder.TRUE
            if len(left) > len(right):
                return InOrder.FALSE
            elif len(right) > len(left):
                return InOrder.TRUE
            return InOrder.UNDECIDED


def part_1(data):
    # for p1, p2 in data:
    #     print(p1)
    #     print(p2)
    #     print(right_order(p1, p2))
    return sum(
        i if right_order(*p) == InOrder.TRUE else 0 for i, p in zip(count(1), data)
    )


def part_2(data):
    flattened_data = list(chain(*data))
    index_2 = (
        sum(1 if right_order(p, [[2]]) == InOrder.TRUE else 0 for p in flattened_data)
        + 1
    )
    index_6 = (
        sum(1 if right_order(p, [[6]]) == InOrder.TRUE else 0 for p in flattened_data)
        + 2
    )
    return index_2 * index_6


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))
