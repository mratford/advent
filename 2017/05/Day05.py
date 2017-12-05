def strange_run(instructions):
    state = instructions.copy()
    pointer = 0
    cpu_cycles = 0
    
    while 0 <= pointer <  len(state):
        next_instruction = pointer + state[pointer]
        
        if state[pointer] >= 3:
            state[pointer] -= 1
        else:
            state[pointer] += 1
            
        cpu_cycles += 1
        pointer = next_instruction
        
    return cpu_cycles

with open('input', 'r') as f:
    instructions = [int(line) for line in f]

print(strange_run(instructions))
