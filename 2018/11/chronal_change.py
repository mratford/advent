from itertools import product, combinations_with_replacement
import numpy as np


def hundreds_digit(x):
    return (x - (x // 1000) * 1000) // 100


def power_level(x, y, serial):
    rack_id = x + 10
    power_level = (rack_id * y + serial) * rack_id
    return(hundreds_digit(power_level)) - 5


def grid(serial_number):
    g = {}

    for x in range(1, 301):
        for y in range(1, 301):
            g[(x, y)] = power_level(x, y, serial_number)

    return g


def n_by_n_coords(x, y, n=3):
    return product(range(x, x + n), range(y, y + n))


def most_powerful_square_of_all(grid):
    maxes = []
    for n in range(1, 301):
        squares = product(range(1, 302 - n), range(1, 302 - n))
        maxes.append(max((sum(grid[p] 
                              for p in n_by_n_coords(sq[0], sq[1], n)), sq, n) 
                         for sq in squares))
        
    return max(maxes)


# Define a 301x301 grid for convenience
def grid_np(serial_number):
    return np.array([[power_level(x, y, serial_number) 
                      for y in range(301)] 
                     for x in range(301)])


def most_powerful_square_of_all_np(grid):
    maxes = []
    return max(max((grid[x:(x+n), y:(y+n)].sum(), x, y, n) 
                    for x, y in product(range(1, 302 - n), range(1, 302 - n)))
               for n in range(1, 301))[1:]


if __name__ == '__main__':
    print(most_powerful_square_of_all_np(grid_np(9810)))
    
