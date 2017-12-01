with open('input', 'r') as f:
    input = [int(x) for x in f.read().strip()]

def sum_tuples_if_equal(ts):
    return sum(x for x, y in ts if x==y)

def circulate(input, offset):
    return zip(input, input[offset:] + input[:offset])

print("Part 1", sum_tuples_if_equal(circulate(input, 1)))

halfway = len(input)//2
print("Part 2", sum_tuples_if_equal(circulate(input, halfway)))
