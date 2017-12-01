count = 0

with open('triangles', 'rt') as f:
    for line in [l.strip() for l in f]:
        sides = sorted([int(i) for i in line.split()])
        if sides[0] + sides[1] > sides[2]:
            count += 1

print(count)
