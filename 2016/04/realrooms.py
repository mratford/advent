import re
from collections import defaultdict


def get_rooms(file_name):
    room_re = re.compile(r"([a-z-]*)(\d*)\[([a-z]*)\]")
    with open(file_name, 'rt') as f:
        for line in f:
            match = room_re.match(line)
            print(match.group(0))
            yield ([c for c in match.group(1) if c != "-"],
                   int(match.group(2)),
                   match.group(3))


def order_letters(name):
    letter_counts = defaultdict(int)
    for letter in name:
        letter_counts[letter] += 1
    return [k for k, v in sorted(letter_counts.items(),
                                 key=lambda kv: (-kv[1], kv[0]))]


running_total = 0

for room in get_rooms("input"):
    name, sector_id, checksum = room
    if order_letters(name)[:5] == list(checksum):
        running_total += sector_id

print(running_total)

