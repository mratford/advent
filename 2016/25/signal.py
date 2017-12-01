from itertools import islice


with open('input','rt') as f:
    prog = [line.strip().split() for line in f]

registers = 'abcd'
reg_values = {r: 0 for r in registers}
reg_values['a'] = 12

def value(x):
    if x in registers:
        return reg_values[x]
    else:
        return int(x)

def run(code_in):
    code = list(code_in)
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
            elif c[0] == 'out':
                yield value(c[1])
        except IndexError:
            pass
        i += 1


for a in [182, 865, 1206, 1889, 2230, 2913, 3254, 3937, 4278, 4961, 5302,
          5985, 6326, 7009, 7350, 8033]:
    n = 1000
    alt_bits = [0, 1] * n
    reg_values = {r: 0 for r in registers}
    reg_values['a'] = a
    x = list(islice(run(prog), n))
    if x == alt_bits[:n] or x == alt_bits[1:n + 1]:
        print(a)
    
