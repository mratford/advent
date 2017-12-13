import parsy
import itertools

integer = parsy.digit.at_least(1).concat().map(int)

def process_data(data):
    parse_depth_range = parsy.seq(integer << parsy.string(': '), integer) \
      .combine(lambda d, r: (d, r))       
    return [parse_depth_range.parse(line.strip())
            for line in data]

def cycle_length(r):
    return 2 * (r - 1)

def severity(firewall):
    return sum([d * r for d, r in firewall
                if d % cycle_length(r) == 0])

def safe(firewall, delay):
    for d, r in firewall:
        if (d + delay) % cycle_length(r) == 0:
            return False
    return True

def first_safe_delay(firewall):
    for delay in itertools.count():
        if safe(firewall, delay):
            return delay

with open('input', 'r') as f:
    input_firewall = process_data(f)
    
print(first_safe_delay(input_firewall))
