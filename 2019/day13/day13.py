import intcode
from pyrsistent import pvector
from itertools import zip_longest
from collections import defaultdict


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def draw_screen(screen):
    icons = {
        0: ' ', # empty
        1: 'X', # wall
        2: '#', # block
        3: '-', # paddle
        4: 'O'  # ball
        }
    
    max_x = max(x for x, y in screen)
    max_y = max(y for x, y in screen)
    
    for y in range(max_y + 1):
        print(''.join(icons[screen[(x, y)]] for x in range(max_x + 1)))


def solve_part_1(code: str) -> int:
    game = intcode.Intcode(code)
    
    screen = defaultdict(int)
    outputs = game.run(pvector())
    
    for x, y, tile_id in grouper(outputs, 3):
        screen[(x, y)] = tile_id
        
    # draw_screen(screen)
        
    return sum(1 for x in screen.values() if x == 2)
    

def solve_part_2(code: str) -> str:
    game = intcode.Intcode(code)
    game.code[0] = 2
    
    screen = defaultdict(int)
    score = 0
    ball = (-1, 0)
    bat = (-1, 0)
    joystick = 0
    
    while True:
        # I doubt this will work (edit: blimey, it does)
        if bat[0] < ball[0]:
            joystick = 1
        elif bat[0] > ball[0]:
            joystick = -1
        else:
            joystick = 0
        
        outputs = game.run(pvector([joystick]))
        
        for x, y, tile_id in grouper(outputs, 3):
            if x == -1 and y == 0:
                score = tile_id
            else:
                screen[(x, y)] = tile_id
                if tile_id == 4:
                    ball = (x, y)
                elif tile_id == 3:
                    bat = (x, y)
                    
        # draw_screen(screen)
        # print(f'Score: {score}')
        # print()
        
        blocks_left = sum(1 for x in screen.values() if x == 2)
        if blocks_left == 0 or ball[1] > bat[1]:
            return f'Score={score}, finished={blocks_left == 0}' 
        
        
if __name__ == '__main__':
    code = open('input', 'r').read().strip()
    print(f'Part 1: {solve_part_1(code)}')
    print(f'Part 2: {solve_part_2(code)}')