from pyrsistent import pvector, pmap
from pyrsistent.typing import PVector, PMap
from collections import defaultdict
from typing import Iterator, List, ClassVar, DefaultDict
from copy import deepcopy


# Create a mask for immediate values from the integer values
def _parameter_mask(n: int) -> Iterator[int]:
    while True:
        n, r = divmod(n, 10)
        yield r
        
        
# Find the memory location of the arguments based on the mask        
def _get_arguments(program: DefaultDict[int, int],
                   pointer: int,
                   relative_base: int,
                   n_args: int,
                   mask: Iterator[int]) -> List[int]:
    args = []
    for p, m in zip(range(pointer, pointer + n_args), mask):
        if m == 0:
            args.append(program[p])
        elif m == 1:
            args.append(p)
        elif m == 2:
            args.append(program[p] + relative_base)

    return args


class Intcode:
    def __init__(self, program: str):
        self.code: DefaultDict[int, int] = defaultdict(int)
        for i, x in enumerate(program.strip().split(',')):
            self.code[i] = int(x)
        self.p: int = 0
        self.relative_base: int = 0
        self.original_code = deepcopy(self.code)
            

    # Right, having to change this. Keep the state, run until either
    # expecting an input or finishing, either way returning a list of outputs.
    def run(self, inputs: PVector[int]) -> PVector[int]:
        inputs_iter = iter(inputs)
        outputs: PVector[int] = pvector()
        
        while self.p in self.code:
            int_mask, opcode = divmod(self.code[self.p], 100)
            param_mask = _parameter_mask(int_mask)
            
            if opcode == 99:
                return outputs
            elif opcode == 1:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 3, param_mask)
                self.code[args[2]] = self.code[args[0]] + self.code[args[1]]
                self.p += 4
            elif opcode == 2:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 3, param_mask)
                self.code[args[2]] = self.code[args[0]] * self.code[args[1]]
                self.p += 4
            elif opcode == 3:
                try:
                    args = _get_arguments(self.code, self.p + 1,
                                          self.relative_base, 1, param_mask)
                    x = next(inputs_iter)
                    self.code[args[0]] = x
                    self.p += 2
                except StopIteration:
                    return outputs
            elif opcode == 4:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 1, param_mask)
                self.p += 2
                outputs = outputs.append(self.code[args[0]])
            elif opcode == 5:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 2, param_mask)
                if self.code[args[0]] != 0:
                    self.p = self.code[args[1]]
                else:
                    self.p += 3
            elif opcode == 6:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 2, param_mask)
                if self.code[args[0]] == 0:
                    self.p = self.code[args[1]]
                else:
                    self.p += 3
            elif opcode == 7:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 3, param_mask)
                self.code[args[2]] = (
                    1 if self.code[args[0]] < self.code[args[1]] else 0)
                self.p += 4
            elif opcode == 8:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 3, param_mask)
                self.code[args[2]] = (
                    1 if self.code[args[0]] == self.code[args[1]] else 0)
                self.p += 4
            elif opcode == 9:
                args = _get_arguments(self.code, self.p + 1,
                                      self.relative_base, 1, param_mask)
                self.relative_base += self.code[args[0]]
                self.p += 2


        return outputs
        

    def reset(self):
        self.code = deepcopy(self.original_code)
        self.p = 0
        self.relative_base = 0

        return self