from copy import deepcopy
from intcode import Intcode
from collections import deque
from pyrsistent import pvector


directions = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}


def answer_part_1(s):
    ship_map = {(0, 0): '.'}
    # Each search state is a tuple of the current state of the program, the
    # location, and the number of moves made. Do a breadth first search
    # until the target is found.
    search = deque([(Intcode(s), (0, 0), 0)])
    
    while True:
        program, coordinate, moves = search.popleft()
        x, y = coordinate
        
        for command in range(1, 5):
            dx, dy = directions[command]
            new_coords = (x + dx, y + dy)
            if new_coords not in ship_map:
                new_program = deepcopy(program)
                status = new_program.run(pvector([command]))[0]

                if status == 0:
                    ship_map[new_coords] = '#'
                elif status == 1:
                    ship_map[new_coords] = '.'
                    search.append((new_program, new_coords, moves + 1))
                elif status == 2:
                    return moves + 1
                
    return None


def get_full_map(s):
    ship_map = {(0, 0): '.'}
    # Each search state is a tuple of the current state of the program, the
    # location, and the number of moves made. Do a breadth first search
    # until all locations are visited.
    search = deque([(Intcode(s), (0, 0), 0)])
    
    while search:
        program, coordinate, moves = search.popleft()
        x, y = coordinate
        
        for command in range(1, 5):
            dx, dy = directions[command]
            new_coords = (x + dx, y + dy)
            if new_coords not in ship_map:
                new_program = deepcopy(program)
                status = new_program.run(pvector([command]))[0]

                if status == 0:
                    ship_map[new_coords] = '#'
                elif status == 1:
                    ship_map[new_coords] = '.'
                    search.append((new_program, new_coords, moves + 1))
                elif status == 2:
                    ship_map[new_coords] = 'O'
                    search.append((new_program, new_coords, moves + 1))
                    
    return ship_map


def answer_part_2(s):
    ship_map = get_full_map(s)
    
    minute = 0
    
    while True:
        new_map = deepcopy(ship_map)
        location_with_no_oxygen = False
        
        for x, y in ship_map:
            if ship_map[(x, y)] == '.':
                location_with_no_oxygen = True
            elif ship_map[(x, y)] == 'O':
                for direction in range(1, 5):
                    dx, dy = directions[direction]
                    new_coords = (x + dx, y + dy)
                    if ship_map[new_coords] == '.':
                        new_map[new_coords] = 'O'
                        
        if not location_with_no_oxygen:
            return minute
        
        minute += 1
        ship_map = new_map

    
if __name__ == '__main__':
    data = open('input', 'r').read()
    print(f'Part 1: {answer_part_1(data)}')
    print(f'Part 2: {answer_part_2(data)}')