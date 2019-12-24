from typing import Tuple, Iterator, Dict, Set
import logging


logging.basicConfig(filename='test.log', filemode='w', level=logging.DEBUG)


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
        step_x = -1 if dx < 0 else 1
        step_y = 0
    elif dx == 0:
        step_x = 0
        step_y = -1 if dy < 0 else 1
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
            
            
def parse(s: str) -> Tuple[Tuple[int, int], Set[Tuple[int, int]]]:
    '''Parses the asteroid field, returning a set of asteroid coordinates
    and the maximum x and y'''
    field = s.splitlines()
    asteroids = {(x, y) 
                 for y, line in enumerate(field)
                 for x, c in enumerate(line)
                 if c == '#'}
    
    return ((len(field[0]), len(field)), asteroids)


def find_monitoring_station(span: Tuple[int, int], 
                            asteroids: Set[Tuple[int, int]]) \
                                -> Tuple[Tuple[int, int], int]:
    max_x, max_y = span
    
    asteroids_detected: Dict[Tuple[int, int], int] = {}
    
    for asteroid in asteroids:
        can_see = {a 
                   for a in asteroids - {asteroid}
                   if len(set(integer_coords(asteroid, a)) & asteroids) == 0}
        asteroids_detected[asteroid] = len(can_see)
        
    monitoring_station = max(asteroids_detected, key=asteroids_detected.get)
    return (monitoring_station, asteroids_detected[monitoring_station])
   


def solve_part_1(s: str) -> int:
    span, asteroids = parse(s)
    return find_monitoring_station(span, asteroids)[1]
    

                   
def solve_part_2(s: str) -> int:
    return -1
    
    
                   
                   
if __name__ == '__main__':
    s = open('input', 'r').read()
    print(f'Part 1: {solve_part_1(s)}')