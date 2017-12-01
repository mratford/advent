disk_size = 35651584
input = '01110110101001000'

state = [bool(int(x)) for x in list(input)]

while len(state) < disk_size:
    state = list(state) + [False] + [not bit for bit in reversed(state)]
    
state = state[:disk_size]

while len(state) % 2 == 0:
    state = [state[i] == state[i+1] for i in range(0, len(state), 2)]

print(''.join(['1' if bit else '0' for bit in state]))
