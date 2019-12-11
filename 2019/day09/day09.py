from intcode import Intcode
from pyrsistent import pvector


if __name__ == '__main__':
    program = open('input', 'r').read().strip()
    print(f'Part 1: {Intcode(program).run(pvector([1]))}')
    print(f'Part 2: {Intcode(program).run(pvector([2]))}')
