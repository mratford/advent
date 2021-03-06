from pyrsistent import pvector
from pyrsistent.typing import PVector
from typing import Iterator, List, ClassVar
import operator
import logging


logging.basicConfig(filename='test.log', filemode='w', level=logging.INFO)


# Create a mask for immediate values from the integer values
def _parameter_mask(n: int) -> Iterator[bool]:
    while True:
        n, r = divmod(n, 10)
        yield bool(r)
        
        
# Find the arguments based on the mask        
def _get_arguments(program: PVector[int], pointer: int, 
                    n_args: int, mask: Iterator[bool]) -> List[int]:
    args = [v if m else program[v]
            for v, m in zip(program[pointer : pointer + n_args], mask)]
    logging.debug(f'Args: {args}')
    return args


class Intcode:
    def __init__(self, program: str):
        self.code: PVector[int] = (
            pvector(int(x) for x in program.strip().split(',')))
        self.p: int = 0


    # Right, having to change this. Keep the state, run until either
    # expecting an input or finishing, either way returning a list of outputs.
    def run(self, inputs: PVector[int]) -> PVector[int]:
        inputs_iter = iter(inputs)
        outputs: PVector[int] = pvector()
        
        while self.p < len(self.code):
            logging.debug(self.p)
            logging.debug(list(enumerate(self.code)))
            int_mask, opcode = divmod(self.code[self.p], 100)
            param_mask = _parameter_mask(int_mask)
            
            if opcode == 99:
                return outputs
            elif opcode == 1:
                self.code = self.code.set(
                    self.code[self.p + 3],
                    operator.add(
                        *_get_arguments(self.code, self.p + 1, 2, param_mask)
                        )
                    )
                
                self.p += 4
            elif opcode == 2:
                self.code = self.code.set(
                    self.code[self.p + 3],
                    operator.mul(
                        *_get_arguments(self.code, self.p + 1, 2, param_mask)
                        )
                )
                self.p += 4
            elif opcode == 3:
                try:
                    x = next(inputs_iter)
                    logging.debug(f'Input: {x}') 
                    self.code = self.code.set(self.code[self.p + 1], x)
                    self.p += 2
                except StopIteration:
                    return outputs
            elif opcode == 4:
                args = _get_arguments(self.code, self.p + 1, 1, param_mask)
                self.p += 2
                logging.debug(f'Output: {args[0]}')
                outputs = outputs.append(args[0])
            elif opcode == 5:
                args = _get_arguments(self.code, self.p + 1, 2, param_mask)
                if args[0] != 0:
                    self.p = args[1]
                else:
                    self.p += 3
            elif opcode == 6:
                args = _get_arguments(self.code, self.p + 1, 2, param_mask)
                if args[0] == 0:
                    self.p = args[1]
                else:
                    self.p += 3
            elif opcode == 7:
                args = _get_arguments(self.code, self.p + 1, 2, param_mask)
                self.code = self.code.set(self.code[self.p + 3],
                                          1 if args[0] < args[1] else 0)
                self.p += 4
            elif opcode == 8:
                args = _get_arguments(self.code, self.p + 1, 2, param_mask)
                self.code = self.code.set(self.code[self.p + 3],
                                          1 if args[0] == args[1] else 0)
                self.p += 4

        return outputs
        

