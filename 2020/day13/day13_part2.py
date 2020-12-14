# Brute force solution for running with pypy, a better
# solution is in the notebook.

import itertools

def parse_data_2(s):
    lines = s.strip().splitlines()
    return {
        (i, int(bus_id))
        for i, bus_id in enumerate(lines[1].split(','))
        if bus_id != 'x'
    }
    
def part_2(data):
    t_delta, bus_id = max(data, key=lambda x: x[1])
    # Make it marginally faster as we don't have to check the
    # bus_id above
    checks = data - {(t_delta, bus_id)}
    timestamps = (bus_id * i - t_delta for i in itertools.count())
    
    for t in timestamps:
        if all(
            (t + t_delta) % bus == 0
            for t_delta, bus in checks
        ):
            return t
        
data_2 = parse_data_2(open('input').read())

print(part_2(data_2))