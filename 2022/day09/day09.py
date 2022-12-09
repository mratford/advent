from dataclasses import dataclass
from typing import Callable, List, Tuple
import pprint


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))


def move_closure() -> Callable[[Point, str], Point]:
    directions = {
        "R": Point(1, 0),
        "L": Point(-1, 0),
        "U": Point(0, 1),
        "D": Point(0, -1),
    }

    def f(p: Point, d: str) -> Point:
        return p + directions[d]

    return f


move = move_closure()


def distance(p1: Point, p2: Point) -> int:
    return max(abs(p1.x - p2.x), abs(p1.y - p2.y))


def move_head_tail(head: Point, tail: Point, direction: str) -> Tuple[Point, Point]:
    new_head = move(head, direction)
    # Move tail into old head position if too far away
    return (new_head, tail if distance(new_head, tail) < 2 else head)


def parse_data(s: str) -> List[Tuple[str, int]]:
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
    pp = pprint.PrettyPrinter(indent=4)
    snake = [Point(0, 0) for _ in range(10)]
    nines = {snake[-1]}

    for d, n in moves:
        for _ in range(n):
            new_snake = [None] * 10
            new_snake[0], new_snake[1] = move_head_tail(snake[0], snake[1], d)
            for i in range(9):
                new_snake[i + 1] = (
                    snake[i + 1]
                    if distance(snake[i + 1], new_snake[i]) < 2
                    else snake[i]
                )
                if i != 8:
                    if distance(new_snake[i + 1], snake[i + 2]) > 1:
                        new_snake[i + 1] = move(snake[i + 1], d)
            snake = new_snake
            nines.add(snake[-1])
        print(d, n)
        pp.pprint(dict(enumerate(snake)))

    return len(nines)


if __name__ == "__main__":
    moves = parse_data(open("test_input_2").read())
    print("Part 1:", part_1(moves))
    print("Part 2:", part_2(moves))
