from pyrsistent import pvector, pmap
from pyrsistent.typing import PVector, PMap
from collections import defaultdict
from typing import Iterator, List, ClassVar, DefaultDict
import operator
import logging


logging.basicConfig(filename='test.log', filemode='w', level=logging.DEBUG)


# Create a mask for immediate values from the integer values
def _parameter_mask(n: int) -> Iterator[int]:
    while True:
        n, r = divmod(n, 10)
        yield r
        
        
# Find the arguments based on the mask        
def _get_arguments(program: DefaultDict[int, int], pointer: int,
                   relative_base: int,
                   n_args: int, mask: Iterator[int]) -> List[int]:
    args = []
    params = [program[p] for p in range(pointer, pointer + n_args)]
    for v, m in zip(params, mask):
        logging.debug((m, v))
        if m == 0:
            args.append(program[v])
        elif m == 1:
            args.append(v)
        elif m == 2:
            args.append(program[v + relative_base])
            
    logging.debug(f'Args: {args}')
    return args


class Intcode:
    def __init__(self, program: str):
        self.code: DefaultDict[int, int] = defaultdict(int)
        for i, x in enumerate(program.strip().split(',')):
            self.code[i] = int(x)
        self.p: int = 0
        self.relative_base: int = 0


    # Right, having to change this. Keep the state, run until either
    # expecting an input or finishing, either way returning a list of outputs.
    def run(self, inputs: PVector[int]) -> PVector[int]:
        inputs_iter = iter(inputs)
        outputs: PVector[int] = pvector()
        
        while self.p in self.code:
            logging.debug(self.p)
            logging.debug(self.code)
            int_mask, opcode = divmod(self.code[self.p], 100)
            param_mask = _parameter_mask(int_mask)
            
            if opcode == 99:
                return outputs
            elif opcode == 1:
                self.code[self.p + 3] = operator.add(
                    *_get_arguments(self.code, self.p + 1,
                                    self.relative_base, 2, param_mask)
                    )
                self.p += 4
            elif opcode == 2:
                self.code[self.p + 3] = operator.mul(
                    *_get_arguments(self.code, self.p + 1,
                                    self.relative_base, 2, param_mask)
                    )
                self.p += 4
            elif opcode == 3:
                try:
                    x = next(inputs_iter)
                    logging.debug(f'Input: {x}') 
                    self.code[self.p + 1] = x
                    self.p += 2
                except StopIteration:
                    return outputs
            elif opcode == 4:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 1, param_mask)
                self.p += 2
                logging.debug(f'Output: {args[0]}')
                outputs = outputs.append(args[0])
            elif opcode == 5:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 2, param_mask)
                if args[0] != 0:
                    self.p = args[1]
                else:
                    self.p += 3
            elif opcode == 6:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 2, param_mask)
                if args[0] == 0:
                    self.p = args[1]
                else:
                    self.p += 3
            elif opcode == 7:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 2, param_mask)
                self.code[self.p + 3] = 1 if args[0] < args[1] else 0
                self.p += 4
            elif opcode == 8:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 2, param_mask)
                self.code[self.p + 3] = 1 if args[0] == args[1] else 0
                self.p += 4
            elif opcode == 9:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 2, param_mask)
                self.relative_base += args[0]
                self.p += 2


        return outputs
        

