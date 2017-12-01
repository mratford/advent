first_row = open('input', 'rt').readline().strip()
#first_row = '.^^.^.^^^^'

def get(row, index):
    if index < 0 or index >= len(row):
        return '.'
    else:
        return row[index]


def count_safe(row):
    return sum([1 if x == '.' else 0 for x in row])

num_safe = count_safe(first_row)
prev = first_row

for i in range(399999):
    nextr = ['^' if get(prev, j - 1) != get(prev, j + 1) else '.'
             for j in range(len(prev))]
    num_safe += count_safe(nextr)
    prev = list(nextr)
    
    

print(num_safe)
