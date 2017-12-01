import re

with open('input', 'rt') as f:
    compressed = f.read().rstrip()

def uncompress(string):
    i = 0
    uncompressed_length = 0
    while i < len(string):
        marker = re.match(r'\((\d+)x(\d+)\)', string[i:])
        if marker:
            length = int(marker.group(1))
            repetitions = int(marker.group(2))
            p = marker.end()
            uncompressed_length += repetitions * \
              uncompress(string[i + p: i + p + length])
            i = i + p + length
        elif string[i].isspace():
            i += 1
        else:
            uncompressed_length += 1
            i += 1
    return uncompressed_length

# print(uncompress("(27x12)(20x12)(13x14)(7x10)(1x12)A"))
# print(uncompress("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"))
print(uncompress(compressed))
