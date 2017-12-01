with open('input','rt') as f:
    code = [line.strip().split() for line in f]

registers = 'abcd'
reg_values = {r: 0 for r in registers}
reg_values['c'] = 1

def value(x):
    if x in registers:
        return reg_values[x]
    else:
        return int(x)
    
i = 0
while i < len(code):
    c = code[i]
    if c[0] == 'cpy':
        reg_values[c[2]] = value(c[1])
        i += 1
    elif c[0] == 'inc':
        reg_values[c[1]] += 1
        i += 1
    elif c[0] == 'dec':
        reg_values[c[1]] -= 1
        i += 1
    elif c[0] == 'jnz':
        if value(c[1]) != 0:
            i += value(c[2])
        else:
            i += 1

print(reg_values['a'])
