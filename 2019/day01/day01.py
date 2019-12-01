from typing import List, TypeVar, Callable, Iterator
import itertools


T = TypeVar('T')


def fuel_needed(mass: int) -> int:
    return max(mass // 3 - 2, 0)


def total_fuel(masses: List[int]) -> int:
    return sum(fuel_needed(mass) for mass in masses)


def repeat(f: Callable[[T], T], x: T) -> Iterator[T]:
    while True:
        yield (x := f(x))


def module_fuel(mass: int) -> int:
    fuels = itertools.takewhile(lambda x: x > 0, repeat(fuel_needed, mass))
    return sum(fuels)


def actual_total_fuel(masses: List[int]) -> int:
    return sum(module_fuel(mass) for mass in masses)


if __name__ == '__main__':
    masses = [int(line.strip()) for line in open('input')]
    fuel_required = total_fuel(masses)
    print(f'Part 1: {fuel_required}')
    actual_fuel = actual_total_fuel(masses)
    print(f'Part 2: {actual_fuel}')

