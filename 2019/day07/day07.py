from intcode import Intcode
import itertools
from typing import Tuple


def run_phase_setting(phases: Tuple[int, ...], code: Intcode) -> int:
    output = 0
    for phase in phases:
        output = next(code.run(iter([phase, output])))
    return output


def solve_part_1(s: str) -> int:
    code = Intcode(s)
    return max(run_phase_setting(phases, code)
               for phases in itertools.permutations(range(5)))
    
    
if __name__ == '__main__':
    program = open('input', 'r').read()
    print(f'Part 1: {solve_part_1(program)}')
    

    