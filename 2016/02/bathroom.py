keypad = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
directions = {'U':(-1, 0), 'D':(1, 0), 'L':(0, -1), 'R':(0, 1)}

def keep_in_pad(p):
    return max(min(p, 2), 0)

with open("instructions.txt", "rt") as f:
    for line in [l.strip() for l in f]:
        position = [1, 1]
        for move in [directions[d] for d in line]:
            position[0] = keep_in_pad(position[0] + move[0])
            position[1] = keep_in_pad(position[1] + move[1])
        print(keypad[position[0]][position[1]])
        
            
            
