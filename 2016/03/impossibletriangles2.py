with open('triangles', 'rt') as f:
    lines = [line.strip().split() for line in f]
    data = [[int(x) for x in line] for line in lines if line]

count = 0

for i in range(0, len(data), 3):
    triangles = data[i:i + 3]
    for j in range(3):
        x, y, z = tuple(sorted([t[j] for t in triangles]))
        if x + y > z:
            count += 1

print(count)
