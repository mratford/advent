keypad = [list(s) for s in 'xx1xx:x234x:56789:xABCx:xxDxx'.split(':')]
directions = {'U':(-1, 0), 'D':(1, 0), 'L':(0, -1), 'R':(0, 1)}

with open("instructions.txt", "rt") as f:
    for line in [l.strip() for l in f]:
        position = [1, 1]
        for move in [directions[d] for d in line]:
            old_position = position[:]
            position[0] = position[0] + move[0]
            position[1] = position[1] + move[1]
            if position[0] not in range(5) or position[1] not in range(5) \
                or keypad[position[0]][position[1]] == 'x':
                position = old_position
        print(keypad[position[0]][position[1]])
        
            
            
