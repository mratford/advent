uncompressed_length = 0

with open('input', 'rt') as f:
    compressed = f.read().rstrip()

def uncompress(string):
    uncompressed_length = 0:
    i = 0
    while i < len(compressed):
            if compressed[i] == '(':
                p = compressed.find(')', i + 1)
                if p > i + 3:
                        marker = [int(x) for x in compressed[i + 1: p].split('x')]
                        length = marker[0]
                        repetitions = marker[1]
                        uncompressed_length += length * repetitions
                        i = p + length + 1
            elif compressed[i].isspace():
                i += 1
            else:
                uncompressed_length += 1
        i += 1

i = 0
while i < len(compressed):
    if compressed[i] == '(':
        p = compressed.find(')', i + 1)
        if p > i + 3:
            marker = [int(x) for x in compressed[i + 1: p].split('x')]
            length = marker[0]
            repetitions = marker[1]
            uncompressed_length += length * repetitions
            i = p + length + 1
    elif compressed[i].isspace():
        i += 1
    else:
        uncompressed_length += 1
        i += 1

print(uncompressed_length)
