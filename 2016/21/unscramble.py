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


def unrotate(s, offset):
    return rotate(s, -offset)


def rotate_on_letter(s, letter):
    i = s.find(letter)
    return rotate(s, -(1 + i + (1 if i >= 4 else 0)))


def unrotate_on_letter(s, letter):
    i = s.find(letter)
    for j in range(len(s)):
        if (i - j) % len(s) == (1 + j + (1 if j >= 4 else 0)) % len(s):
            return rotate(s, (i - j) % len(s))


def move(s, pos1, pos2):
    letter = s[pos1]
    t = s[:pos1] + s[pos1 + 1:]
    return t[:pos2] + letter + t[pos2:]


def unmove(s, pos1, pos2):
    return move(s, pos2, pos1)


def parse(message, command):
    m = re.match(r'(swap position) (\d+) with position (\d+)', command)
    if m:
        return swap_positions(message, int(m.group(2)), int(m.group(3)))
    m = re.match(r'(swap letter) (\w) with letter (\w)', command)
    if m:
        return swap_letters(message, m.group(2), m.group(3))
    m = re.match(r'(rotate based) on position of letter (\w)', command)
    if m:
        return unrotate_on_letter(message, m.group(2))
    m = re.match(r'(rotate) (?P<direction>\w+) (\d+)', command)
    if m:
        offset = int(m.group(3))
        return unrotate(message,
                        offset if m.group('direction') == 'left' else -offset)
    m = re.match(r'(reverse) positions (\d+) through (\d+)', command)
    if m:
        return reverse(message, int(m.group(2)), int(m.group(3)))
    m = re.match(r'(move) position (\d+) to position (\d+)', command)
    if m:
        return unmove(message, int(m.group(2)), int(m.group(3)))

    
message = 'fbgdceah'
with open('input', 'rt') as f:
    for command in reversed(f.readlines()):
        message = parse(message, command)
print(message)
