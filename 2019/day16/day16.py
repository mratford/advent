import itertools, functools


def parse_data(s):
    return [int(x) for x in s.strip()]


def pattern(element_index):
    base_pattern = [0, 1, 0, -1]
    return list(itertools.chain.from_iterable(
        itertools.repeat(x, element_index) for x in base_pattern
    ))
    
    
def phase(l):
    return [
        abs(n) % 10 for n in (
            sum(
                x * y 
                for x, y in zip(
                    itertools.islice(itertools.cycle(pattern(i)), 1, None), 
                    l
                ) 
            )
            for i, e in zip(itertools.count(1), l)
        )
    ]


def answer_part_1(s):
    l = parse_data(s)
    
    for _ in range(100):
        l = phase(l)
        
    return ''.join(str(x) for x in l[:8])
    

if __name__ == '__main__':
    data = open('input', 'r').read()
    print(f'Part 1: {answer_part_1(data)}')
#    print(f'Part 2: {answer_part_2(data)}')