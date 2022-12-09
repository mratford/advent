from dataclasses import dataclass
import pprint


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

    def unit(self):
        if self.x < 0:
            unit_x = -1
        elif self.x == 0:
            unit_x = 0
        else:
            unit_x = 1
        if self.y < 0:
            unit_y = -1
        elif self.y == 0:
            unit_y = 0
        else:
            unit_y = 1
        return self.__class__(unit_x, unit_y)


def move_closure():
    directions = {
        "R": Point(1, 0),
        "L": Point(-1, 0),
        "U": Point(0, 1),
        "D": Point(0, -1),
    }

    def f(p, d):
        return p + directions[d]

    return f


move = move_closure()


def distance(p1, p2):
    return max(abs(p1.x - p2.x), abs(p1.y - p2.y))


def move_towards_head(head, tail):
    return tail + (head - tail).unit()


def move_tail_if_necessary(head, tail):
    return tail if distance(head, tail) < 2 else move_towards_head(head, tail)


def move_head_tail(head, tail, direction):
    new_head = move(head, direction)
    # Move tail into old head position if too far away
    return (new_head, move_tail_if_necessary(head, tail))


def parse_data(s):
    return [(sp[0], int(sp[1])) for sp in [x.split() for x in s.strip().splitlines()]]


def part_1(moves):
    head = Point(0, 0)
    tail = Point(0, 0)
    tails = {tail}

    for d, n in moves:
        for _ in range(n):
            head, tail = move_head_tail(head, tail, d)
            tails.add(tail)

    return len(tails)


def part_2(moves):
    # pp = pprint.PrettyPrinter(indent=4)
    snake = [Point(0, 0) for _ in range(10)]
    nines = {snake[-1]}

    for d, n in moves:
        for _ in range(n):
            snake[0] = move(snake[0], d)
            for i in range(9):
                snake[i + 1] = move_tail_if_necessary(snake[i], snake[i + 1])
            nines.add(snake[-1])
        # print(d, n)
        # pp.pprint(dict(enumerate(snake)))

    return len(nines)


if __name__ == "__main__":
    moves = parse_data(open("input").read())
    print("Part 1:", part_1(moves))
    print("Part 2:", part_2(moves))
