import itertools
import operator
from pyrsistent import pvector
from collections import namedtuple
import logging


logging.basicConfig(filename='test.log', filemode='w', level=logging.DEBUG)


# Create a mask for immediate values from the integer values
def parameter_mask(n):
    while True:
        n, r = divmod(n, 10)
        yield bool(r)
        
        
# Find the arguments based on the mask        
def get_arguments(program, pointer, n_args, mask):
    return [v if m else program[v] 
            for v, m in zip(program[pointer : pointer + n_args], mask)]


# Horribly inelegant code to run through each possible instruction.
# I'm putting  the output as a generator for possible generality.
def intcode(program, input):
    p = 0
    
    while p < len(program):
        logging.debug(f'position={p}\nprogram={program}\n')
        int_mask, opcode = divmod(program[p], 100)
        param_mask = parameter_mask(int_mask)
        
        if opcode == 99:
            return
        elif opcode == 1:
            program = program.set(
                program[p + 3],
                operator.add(
                    *get_arguments(program, p + 1, 2, param_mask)
                    )
                )
            
            p += 4
        elif opcode == 2:
            program = program.set(
                program[p + 3],
                operator.mul(
                    *get_arguments(program, p + 1, 2, param_mask)
                    )
            )
            p += 4
        elif opcode == 3:
            program = program.set(program[p + 1], input)
            p += 2
        elif opcode == 4:
            yield get_arguments(program, p + 1, 1, param_mask)[0]
            p += 2
        elif opcode == 5:
            args = get_arguments(program, p + 1, 2, param_mask)
            if args[0] != 0:
                p = args[1]
            else:
                p += 3
        elif opcode == 6:
            args = get_arguments(program, p + 1, 2, param_mask)
            if args[0] == 0:
                p = args[1]
            else:
                p += 3
        elif opcode == 7:
            args = get_arguments(program, p + 1, 2, param_mask)
            program = program.set(program[p + 3],
                                  1 if args[0] < args[1] else 0)
            p += 4
        elif opcode == 8:
            args = get_arguments(program, p + 1, 2, param_mask)
            program = program.set(program[p + 3],
                                  1 if args[0] == args[1] else 0)
            p += 4
            
                                    

if __name__ == '__main__':
    program = pvector([int(x) for x in open('input', 'r').read().split(',')])
    
    print('Part 1')
    for x in intcode(program, 1):
        print(x)
        
    print('\nPart 2')
    for x in intcode(program, 5):
        print(x)
