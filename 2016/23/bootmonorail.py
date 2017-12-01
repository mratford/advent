with open('input','rt') as f:
    code = [line.strip().split() for line in f]

registers = 'abcd'
reg_values = {r: 0 for r in registers}
reg_values['a'] = 12

def value(x):
    if x in registers:
        return reg_values[x]
    else:
        return int(x)
    
i = 0
while i < len(code):
    try:
        c = code[i]
        if c[0] == 'cpy':
            reg_values[c[2]] = value(c[1])
        elif c[0] == 'inc':
            reg_values[c[1]] += 1
        elif c[0] == 'dec':
            reg_values[c[1]] -= 1
        elif c[0] == 'jnz':
            if value(c[1]) != 0:
                i += value(c[2]) - 1
        elif c[0] == 'tgl':
            print(reg_values)
            j = i + value(c[1])
            if len(code[j]) == 2:
                if code[j][0] == 'inc':
                    code[j][0] = 'dec'
                else:
                    code[j][0] = 'inc'
            elif code[j][0] == 'jnz':
                code[j][0] = 'cpy'
            else:
                code[j][0] = 'jnz'
            for c in code: print(c)
    except IndexError:
        pass
    i += 1

print(reg_values['a'])
