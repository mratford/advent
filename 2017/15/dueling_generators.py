import functools
import itertools


def generator(divisor, factor, start):
    while True:
        start = (start * factor) % divisor
        yield start
        
dueling_generator = functools.partial(generator, 2147483647)

LOWEST_16_BITS_ON = 2**16 - 1

def lowest_16_bits(x):
    return x & LOWEST_16_BITS_ON

def forty_million_duels(gen_a, gen_b):
    return sum(1 for a, b in itertools.islice(zip(gen_a, gen_b), 40000000)
               if lowest_16_bits(a) == lowest_16_bits(b))

test_generator_a = dueling_generator(16807, 65)
test_generator_b = dueling_generator(48271, 8921)

print(forty_million_duels(test_generator_a, test_generator_b))
