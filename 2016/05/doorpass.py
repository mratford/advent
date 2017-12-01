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

password = ''
index = 0

while len(password) < 8:
    m = hashlib.md5()
    m.update((door_id + str(index)).encode('utf-8'))
    h = m.hexdigest()
    if h[:5] == '00000':
        password += h[5]
    index += 1

print(password)
