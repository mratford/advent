import re


def swap_positions(s, pos1, pos2):
    if pos1 > pos2:
        pos1, pos2 = pos2, pos1
    return s[:pos1] + s[pos2] + s[pos1 + 1:pos2] + s[pos1] + s[pos2 + 1:]

    
def swap_letters(s, letter1, letter2):
    i, j = s.find(letter1), s.find(letter2)
    return swap_positions(s, i, j)


def reverse(s, start, finish):
    return s[:start] + ''.join(reversed(s[start:finish + 1])) + s[finish + 1:]


def rotate(s, offset):
    offset = offset % len(s)
    return s[offset:] + s[:offset]


def move(s, pos1, pos2):
    letter = s[pos1]
    t = s[:pos1] + s[pos1 + 1:]
    return t[:pos2] + letter + t[pos2:]

def rotate_on_letter(s, letter):
    i = s.find(letter)
    return rotate(s, -(1 + i + (1 if i >= 4 else 0)))


def parse(message, command):
    m = re.match(r'(swap position) (\d+) with position (\d+)', command)
    if m:
        return swap_positions(message, int(m.group(2)), int(m.group(3)))
    m = re.match(r'(swap letter) (\w) with letter (\w)', command)
    if m:
        return swap_letters(message, m.group(2), m.group(3))
    m = re.match(r'(rotate based) on position of letter (\w)', command)
    if m:
        return rotate_on_letter(message, m.group(2))
    m = re.match(r'(rotate) (?P<direction>\w+) (\d+)', command)
    if m:
        offset = int(m.group(3))
        return rotate(message,
                      offset if m.group('direction') == 'left' else -offset)
    m = re.match(r'(reverse) positions (\d+) through (\d+)', command)
    if m:
        return reverse(message, int(m.group(2)), int(m.group(3)))
    m = re.match(r'(move) position (\d+) to position (\d+)', command)
    if m:
        return move(message, int(m.group(2)), int(m.group(3)))

    
message = 'abcdefgh'
with open('input', 'rt') as f:
    for command in f:
        message = parse(message, command)
print(message)
