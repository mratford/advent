from functools import reduce

with open('input', 'rt') as f:
    blocks = [tuple([int(x) for x in line.strip().split('-')]) for line in f]

def add_block(blocked_ips, new_block):
    if not blocked_ips:
        return [new_block]
    else:
        start, finish = blocked_ips[0]
        new_start, new_finish = new_block
        if finish < new_start - 1:
            return blocked_ips[:1] + add_block(blocked_ips[1:], new_block)
        elif new_finish < start - 1:
            return [new_block] + blocked_ips
        else:
            return add_block(blocked_ips[1:], (min(start, new_start),
                                               max(finish, new_finish)))

def compress_blocks(blocks):
    lowest_block = reduce(add_block, blocks, [])[0]

    if lowest_block[0] > 0:
        return 0
    else:
        return lowest_block[1] + 1

def count_allowed_ips(blocks):
    return 4294967296 - sum([y - x + 1
                             for x, y in reduce(add_block, blocks, [])])

print(compress_blocks(blocks))
print(count_allowed_ips(blocks))

