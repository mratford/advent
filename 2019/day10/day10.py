from typing import Tuple, Iterator, Dict, Set, List
import logging
import math


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


def find_monitoring_station(asteroids: Set[Tuple[int, int]]) \
                                -> Tuple[Tuple[int, int], int]:
    asteroids_detected: Dict[Tuple[int, int], int] = {}
    
    for asteroid in asteroids:
        can_see = {a 
                   for a in asteroids - {asteroid}
                   if len(set(integer_coords(asteroid, a)) & asteroids) == 0}
        asteroids_detected[asteroid] = len(can_see)
        
    monitoring_station = max(asteroids_detected, key=asteroids_detected.get)
    return (monitoring_station, asteroids_detected[monitoring_station])
   


def solve_part_1(s: str) -> int:
    _, asteroids = parse(s)
    return find_monitoring_station(asteroids)[1]



def angle_from_n(o, a):
    # Restate coordinates as normal x, y rather than column, row
    o_x, o_y = o
    o_y = -o_y
    a_x, a_y = a
    a_y = -a_y
       
    # Negate as the angle should go "clockwise"
    angle_from_e = -math.atan2(a_y - o_y, a_x - o_x)
    if angle_from_e < 0:
        angle_from_e += 2*math.pi
    # Add pi/2 to get angle from north
    result = angle_from_e + math.pi/2
    # Correct if overshot 2pi
    return result if result < 2*math.pi else result - 2*math.pi


def zapped_asteroids(monitoring_station: Tuple[int, int], 
                     asteroids: Set[Tuple[int, int]], 
                     max_y: int) -> List[Tuple[int, int]]:
    zapped = []
    asteroids = asteroids - {monitoring_station}
    
    while asteroids:
        can_see = [a for a in asteroids 
                   if len(set(integer_coords(monitoring_station, a)) 
                          & asteroids) == 0]
        
        for a in sorted(can_see, 
                        key=lambda x: angle_from_n(monitoring_station, x)):
            zapped.append(a)
            
        asteroids = asteroids - set(can_see)
            
    return zapped
    

def solve_part_2(s: str) -> int:
    span, asteroids = parse(s)
    _, max_y = span
    monitoring_station = find_monitoring_station(asteroids)[0]
    x, y = zapped_asteroids(monitoring_station, asteroids, max_y)[199]
    return x * 100 + y
                   
                   
if __name__ == '__main__':
    s = open('input', 'r').read()
    print(f'Part 1: {solve_part_1(s)}')
    print(f'Part 2: {solve_part_2(s)}')