from collections import defaultdict


cols = defaultdict(lambda: defaultdict(int))
answer = ''

with open('input', 'rt') as f:
    for line in [l.strip() for l in f]:
        for i in range(len(line)):
            cols[i][line[i]] += 1

for i in sorted(cols):
    answer += min(cols[i], key=cols[i].get)

print(answer)
