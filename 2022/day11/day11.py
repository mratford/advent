from dataclasses import dataclass
from typing import Callable
import math


@dataclass
class Monkey:
    items: list
    operation: Callable[int, int]
    test: Callable[int, bool]
    if_true: int
    if_false: int
    divisor: int

    inspections: int = 0


def parse_data(s):
    monkeys = []
    monkey_inputs = s.strip().split("\n\n")

    for monkey in monkey_inputs:
        monkey_data = monkey.strip().splitlines()
        items = [int(x) for x in monkey_data[1].split(": ")[1].split(", ")]
        operation = eval(f"lambda old: {monkey_data[2].split(' = ')[1]}")
        divisor = int(monkey_data[3].split()[-1])
        test = eval(f"lambda x: x % {divisor} == 0")
        if_true = int(monkey_data[4].split()[-1])
        if_false = int(monkey_data[5].split()[-1])
        monkeys.append(Monkey(items, operation, test, if_true, if_false, divisor))

    return monkeys


def monkey_around(monkeys):
    for i, monkey in enumerate(monkeys):
        for worry_level in monkey.items:
            worry_level = monkey.operation(worry_level) // 3
            if monkey.test(worry_level):
                monkeys[monkey.if_true].items.append(worry_level)
            else:
                monkeys[monkey.if_false].items.append(worry_level)
            monkey.inspections += 1
            monkey.items = []
    return monkeys


def monkey_around_2(monkeys, big_divisor):
    for i, monkey in enumerate(monkeys):
        for worry_level in monkey.items:
            worry_level = monkey.operation(worry_level) % big_divisor
            if monkey.test(worry_level):
                monkeys[monkey.if_true].items.append(worry_level)
            else:
                monkeys[monkey.if_false].items.append(worry_level)
            monkey.inspections += 1
            monkey.items = []
    return monkeys


def part_1(monkeys):
    for _ in range(20):
        monkey_around(monkeys)
    inspections = [monkey.inspections for monkey in monkeys]
    sorted_inspections = sorted(inspections, reverse=True)
    return sorted_inspections[0] * sorted_inspections[1]


def part_2(monkeys):
    # This was making my computer cry so at each stage get the modulus of the
    # worry level w.r.t. the product of the square of each of the divisors -
    # need to use the square so the division conditions still hold.
    big_divisor = math.prod(monkey.divisor**2 for monkey in monkeys)
    for _ in range(10000):
        monkey_around_2(monkeys, big_divisor)
    inspections = [monkey.inspections for monkey in monkeys]
    sorted_inspections = sorted(inspections, reverse=True)
    return sorted_inspections[0] * sorted_inspections[1]


if __name__ == "__main__":
    monkeys = parse_data(open("input").read())
    print("Part 1:", part_1(monkeys))
    monkeys_2 = parse_data(open("input").read())
    print("Part 2:", part_2(monkeys_2))
