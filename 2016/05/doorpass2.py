# doorpass.py
'''
Generate password from Door ID.
'''

import hashlib
import argparse

parser = argparse.ArgumentParser(description='Password generator')
parser.add_argument(dest='door_id', metavar='Door ID')
args = parser.parse_args()
door_id = args.door_id

password = [False for i in range(8)]
i = 0

while not all(password):
    m = hashlib.md5()
    m.update((door_id + str(i)).encode('utf-8'))
    h = m.hexdigest()
    if h[:5] == '00000':
        index = int(h[5], 16)
        if index < 8 and not password[index]:
            password[index] = h[6]
            print(i, index, h[6])
    i += 1

print(''.join(password))
