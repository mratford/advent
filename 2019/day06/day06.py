from collections import defaultdict, deque
from pyrsistent import pmap, pvector, pset
import logging


def parse_orbits(s):
    # Create a graph of orbiting planets from a string, 
    # represented as a dictionary
    orbits = pmap()
    for line in s.splitlines():
        xs = line.strip().split(')')
        orbits = orbits.set(
            xs[0], 
            orbits.get(xs[0], pvector()).append(xs[1])
        )
    return orbits
                


def n_orbits(orbits, planet):
    # Recursively calculate the number of orbits around a planet
    return (len(orbits.get(planet, [])) + 
            sum(n_orbits(orbits, orbiter) 
                for orbiter in orbits.get(planet, [])))



def solve_part_1(orbits):
    return sum(n_orbits(orbits, planet) for planet in orbits)


def shortest_path_length(paths, start, end):
    # Breadth-first search
    
    visited = {start}
    search = deque([(start, 0)])
    
    while search:
        planet, length = search.popleft()
        
        for next_planet in paths[planet]:
            if next_planet == end:
                return length + 1
            elif next_planet not in visited:
                visited.add(next_planet)
                search.append((next_planet, length + 1))
    


def solve_part_2(orbits):
    # Create a bi-directional graph of connected planets
    paths = orbits
    
    for planet in orbits:
        for orbiter in orbits[planet]:
            paths = paths.set(
                orbiter, 
                paths.get(orbiter, pvector()).append(planet)
            )
            
    # Subtract 2 as the paths from "YOU" and "SAN" to planets don't count for
    # the answer
    return shortest_path_length(paths, 'YOU', 'SAN') - 2


if __name__ == '__main__':
    orbits = parse_orbits(open('input', 'r').read())
    print(f'Part 1: {solve_part_1(orbits)}')
    print(f'Part 2: {solve_part_2(orbits)}')
        


