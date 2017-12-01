import re

def supports_ssl(address):
    abas = set()
    babs = set()
    subaddrs = re.split('\[|\]', address)
    for supernet in subaddrs[0::2]:
        abas |= get_xyxs(supernet)
    for hypernet in subaddrs[1::2]:
        babs |= get_xyxs(hypernet)
    return abas & {(y, x) for (x, y) in babs}

def get_xyxs(string):
    result = set()
    for i in range(len(string) - 2):
        if string[i] == string[i + 2] and string[i] != string[i + 1]:
            result.add((string[i], string[i + 1]))
    return result

count = 0

with open('input', 'rt') as f:
    for address in [l.strip() for l in f]:
        if supports_ssl(address):
            count += 1

print(count)
