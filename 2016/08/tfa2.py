width = 50
height = 6
screen = [[0 for y in range(height)] for x in range(width)]


with open('input', 'rt') as f:
    for fields in [l.strip().split() for l in f]:
        print(' '.join(fields))
        if fields[0] == 'rect':
            coords = [int(c) for c in fields[1].split('x')]
            for x in range(coords[0]):
                for y in range(coords[1]):
                    screen[x][y] = 1
        else:  # rotate
            coord = int(fields[2].split('=')[1])
            offset = int(fields[4])
            if fields[1] == 'column':
                new_col = screen[coord][-offset:] + screen[coord][:-offset]
                screen[coord] = new_col[:]
            else:  # row
                old_row = [screen[x][coord] for x in range(width)]
                new_row = old_row[-offset:] + old_row[:-offset]
                for x in range(width):
                    screen[x][coord] = new_row[x]
        print('\n'.join([' '.join([str(screen[x][y]) for x in range(width)])
                         for y in range(height)]) + '\n')

print(sum([sum(col) for col in screen]))

for y in range(height):
    print(''.join([('*' if screen[i][y] else ' ')
                   for i in range(width)]))
