with open('input', 'r') as f:
    input = [int(x) for x in f.read().strip()]

def sum_tuples_if_equal(ts):
    return sum(x for x, y in ts if x==y)

print("Part 1", sum_tuples_if_equal(zip(input, input[1:] + [input[-1]])))

split = len(input)//2
print("Part 2", sum_tuples_if_equal(zip(input, input[split:] + input[:split])))
