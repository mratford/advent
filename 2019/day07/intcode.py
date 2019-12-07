from pyrsistent import pvector
from pyrsistent.typing import PVector
from typing import Iterator, List, ClassVar
import operator


# Create a mask for immediate values from the integer values
def _parameter_mask(n: int) -> Iterator[bool]:
    while True:
        n, r = divmod(n, 10)
        yield bool(r)
        
        
# Find the arguments based on the mask        
def _get_arguments(program: PVector[int], pointer: int, 
                    n_args: int, mask: Iterator[bool]) -> List[int]:
    return [v if m else program[v]
            for v, m in zip(program[pointer : pointer + n_args], mask)]


class Intcode:
    def __init__(self, program: str):
        self.code: PVector[int] = (
            pvector(int(x) for x in program.strip().split(',')))


    # Horribly inelegant code to run through each possible instruction.
    # I'm putting the input as an iterator and the output as a generator
    # for possible generality.
    def run(self, input_iter: Iterator[int]) -> Iterator[int]:
        p = 0
        program = self.code
        
        while p < len(program):
            int_mask, opcode = divmod(program[p], 100)
            param_mask = _parameter_mask(int_mask)
            
            if opcode == 99:
                return
            elif opcode == 1:
                program = program.set(
                    program[p + 3],
                    operator.add(
                        *_get_arguments(program, p + 1, 2, param_mask)
                        )
                    )
                
                p += 4
            elif opcode == 2:
                program = program.set(
                    program[p + 3],
                    operator.mul(
                        *_get_arguments(program, p + 1, 2, param_mask)
                        )
                )
                p += 4
            elif opcode == 3:
                program = program.set(program[p + 1], next(input_iter))
                p += 2
            elif opcode == 4:
                yield _get_arguments(program, p + 1, 1, param_mask)[0]
                p += 2
            elif opcode == 5:
                args = _get_arguments(program, p + 1, 2, param_mask)
                if args[0] != 0:
                    p = args[1]
                else:
                    p += 3
            elif opcode == 6:
                args = _get_arguments(program, p + 1, 2, param_mask)
                if args[0] == 0:
                    p = args[1]
                else:
                    p += 3
            elif opcode == 7:
                args = _get_arguments(program, p + 1, 2, param_mask)
                program = program.set(program[p + 3],
                                      1 if args[0] < args[1] else 0)
                p += 4
            elif opcode == 8:
                args = _get_arguments(program, p + 1, 2, param_mask)
                program = program.set(program[p + 3],
                                      1 if args[0] == args[1] else 0)
                p += 4
