from itertools import cycle, islice
from pyrsistent import pvector 
from functools import reduce
import operator


def cget(v, i):
    return v[i % len(v)]


def cset(v, i, val):
    return v.set(i % len(v), val)


def cslice(v, start, stop):
    # This starts getting slow for large numbers,
    # so minimise the number of cycles produced.
    length = stop - start
    start = start % len(v)
    return islice(cycle(v), start, start + length)


def knot_step(string, length, current):
    r = reversed(pvector(cslice(string, current, current + length)))
    result = pvector(string)
    for i, c in zip(range(current, current + length), r):
        result = cset(result, i, c)
    return result


def knot(string, lengths, rounds=1):
    current = 0
    skip = 0
    
    for i in range(rounds):
        for length in lengths:
            string = knot_step(string, length, current)
            current = current + length + skip
            skip += 1
        
    return string


def ascii_codes(xs):
    return [ord(x) for x in xs]


def length_sequence(s):
    return ascii_codes(s) + [17, 31, 73, 47, 23]


def split_by_length(xs, length):
    for i in range(0, len(xs), length):
        yield xs[i:i+length]


def dense_hash(sparse_hash):
    for xs in split_by_length(sparse_hash, 16):
        yield reduce(operator.xor, xs)


def knot_hash(xs):
    return ''.join((['%02x' % x
                     for x in dense_hash(knot(pvector(range(256)),
                                              length_sequence(xs), 64))]))
