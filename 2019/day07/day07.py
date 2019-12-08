from intcode import Intcode
from itertools import islice, cycle, permutations
from typing import Tuple, List
from pyrsistent import pvector
from pyrsistent.typing import PVector



def run_phase_setting(phases: Tuple[int, ...], program: str) -> int:
    output = 0
    for phase in phases:
        code = Intcode(program)
        output = code.run(pvector([phase, output]))[-1]
    return output


def solve_part_1(code: str) -> int:
    return max(run_phase_setting(phases, code)
               for phases in permutations(range(5)))


def run_phase_setting_2(phases: Tuple[int, ...], program: str) -> int:
    amps = [Intcode(program) for _ in range(5)]
    
    for i, phase in enumerate(phases):
        assert list(amps[i].run(pvector([phase]))) == []
        
    outputs: List[PVector[int]] = [pvector() for _ in range(5)]
    outputs[0] = amps[0].run(pvector([0]))
    
    # Input output 0 to amplifier 1 and carry on
    for i in cycle([1, 2, 3, 4, 0]):
        output = amps[i].run(outputs[i - 1 % 5])
        if output:
            outputs[i] = output
        else:
            break

    return outputs[-1][-1]
            

def solve_part_2(code: str) -> int:
    return max(run_phase_setting_2(phases, code)
               for phases in permutations(range(5, 10)))    

    
if __name__ == '__main__':
    program = open('input', 'r').read()
    print(f'Part 1: {solve_part_1(program)}')
    print(f'Part 2: {solve_part_2(program)}')
    

    
