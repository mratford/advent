from collections import defaultdict
from pyrsistent import pmap, pvector


def read_orbits(fo):
    orbits = pmap()
    for line in fo:
        xs = line.strip().split(')')
        orbits = orbits.set(
            xs[0], 
            orbits.get(xs[0], pvector()).append(xs[1])
        )
    return orbits
                


def n_orbits(orbits, planet):
    return (len(orbits.get(planet, [])) + 
            sum(n_orbits(orbits, orbiter) 
                for orbiter in orbits.get(planet, [])))



def solve_part_1(orbits):
    return sum(n_orbits(orbits, planet) for planet in orbits)


if __name__ == '__main__':
    orbits = read_orbits(open('input', 'r'))
    print(f'Part 1: {solve_part_1(orbits)}')
        


