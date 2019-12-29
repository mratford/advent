from intcode import Intcode
import numpy as np
from pyrsistent import pvector
from itertools import zip_longest, count
from collections import defaultdict
import logging


logging.basicConfig(filename='test.log', filemode='w', level=logging.INFO)


# From itertools recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def solve_part_1(code):
    # Direction
    dx = 0
    dy = 1
    # Position of robot
    px = 0
    py = 0
    # Squares painted
    squares = {}
    
    program = Intcode(code)
    
    for i in count():
        logging.debug(f'{i}')
        logging.debug(len(squares))
        moves = program.run(pvector([squares.get((px, py), 0)]))
        logging.debug(moves)
        if len(moves) == 0:
            break
        
        for move in grouper(moves, 2):
            colour, turn = tuple(move)
            squares[(px, py)] = colour
            if turn == 0: # turn left
                dx, dy = -dy, dx
            else: # turn right
                dx, dy = dy, -dx
            px += dx
            py += dy
            
    return(len(squares))
    
def solve_part_2(code):
    # Direction
    dx = 0
    dy = 1
    # Position of robot
    px = 0
    py = 0
    # Squares painted
    squares = {(0, 0): 1}
    
    program = Intcode(code)
    
    for i in count():
        logging.debug(f'{i}')
        logging.debug(len(squares))
        moves = program.run(pvector([squares.get((px, py), 0)]))
        logging.debug(moves)
        if len(moves) == 0:
            break
        
        for move in grouper(moves, 2):
            colour, turn = tuple(move)
            squares[(px, py)] = colour
            if turn == 0: # turn left
                dx, dy = -dy, dx
            else: # turn right
                dx, dy = dy, -dx
            px += dx
            py += dy

    xs = [sq[0] for sq in squares]
    ys = [sq[1] for sq in squares]
    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)
    
    result = ''
    for y in range(max_y, min_y - 1, -1):
        result += ''.join(['#' if squares.get((x, y), 0) == 1 else ' '
                           for x in range(min_x, max_x + 1)]) +'\n'
        
    return result

    
if __name__ == '__main__':
    code = open('input', 'r').read().strip()
    print(f'Part 1: {solve_part_1(code)}')
    print(f'Part 2:\n{solve_part_2(code)}')