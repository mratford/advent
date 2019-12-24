from typing import Tuple, Iterator, Dict


def abs_gcd(x: int, y: int) -> int:
    'Absolute greatest common denominator'
    while y != 0:
        t = y
        y = x % y
        x = t
    return abs(x)


def integer_coords(a: Tuple[int, int], b: Tuple[int, int]) \
        -> Iterator[Tuple[int, int]]:
    'Return integral coordinate points between but not including a and b'
    from_x, from_y = a
    to_x, to_y = b
    dx = to_x - from_x
    dy = to_y - from_y

    if dy == 0:
        step_x = 1
        step_y = 0
    elif dx == 0:
        step_x = 0
        step_y = 1
    else:
        gcd = abs_gcd(dx, dy)
        step_x = dx // gcd
        step_y = dy // gcd
    
    while True:
        from_x = from_x + step_x
        from_y = from_y + step_y
        
        if from_x == to_x and from_y == to_y:
            return
        else:
            yield (from_x, from_y)
            
            
def parse(s):
    '''Parses the asteroid field, returming a set of asteroid coordinates
    and the maximum x and y'''
    field = s.splitlines()
    asteroids = {(x, y) 
                 for y, line in enumerate(field)
                 for x, c in enumerate(line)
                 if c == '#'}
    
    return ((len(field[0]), len(field)), asteroids)


def solve_part_1(s: str) -> int:
    (max_x, max_y), asteroids = parse(s)

    asteroids_detected: Dict[Tuple[int, int], int] = {}
    
    for asteroid in asteroids:
        can_see = {a 
                   for a in asteroids - {asteroid}
                   if len(set(integer_coords(asteroid, a)) & asteroids) == 0}
        asteroids_detected[asteroid] = len(can_see)
        
    return(max(asteroids_detected.values()))
                   