from pyrsistent import pvector
from pyrsistent.typing import PVector


def run_program(program: PVector[int]) -> PVector[int]:
    for p in range(0, len(program), 4):
        if program[p] == 99:
            return program
        elif program[p] == 1:
            program = program.set(program[p + 3], 
                                  program[program[p + 1]] + program[program[p + 2]])
        elif program[p] == 2:
            program = program.set(program[p + 3], 
                                  program[program[p + 1]] * program[program[p + 2]])

    return program
    

def find_noun_verb(program: PVector[int], match: int) -> int:
    for noun in range(100):
        for verb in range(100):
            p = run_program(program.set(1, noun).set(2, verb))
            if p[0] == match:
                return 100 * noun + verb
            
    return 0


if __name__ == '__main__':
    program = (pvector([int(x) for x in open('input', 'r').read().split(',')])
               .set(1, 12)
               .set(2, 2))

    # print(run_program(pvector([1,9,10,3,2,3,11,0,99,30,40,50])))
    print(f'Part 1: {run_program(program)[0]}')
    print(f'Part 2: {find_noun_verb(program, 19690720)}')
 