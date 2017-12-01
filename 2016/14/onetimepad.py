import hashlib
from functools import lru_cache

# salt = 'abc'
salt = 'ihaygndm'

@lru_cache(maxsize=1024)
def hash(slt, idx):
    m = hashlib.md5()
    m.update((slt + str(idx)).encode('utf-8'))
    for i in range(2016):
        x = m.hexdigest().encode('utf-8')
        m = hashlib.md5()
        m.update(x)
    return m.hexdigest()

def find_triple(s):
    for i in range(len(s) - 2):
        if s[i:i + 3] == s[i] * 3:
            return s[i]

def n_chars_found(n, c, idxs):
    fiver = c * n
    for i in idxs:
        if fiver in hash(salt, i):
            return True
    return False


keys_found = 0
index = 0
while True:
    c = find_triple(hash(salt, index))
    if c:
        if n_chars_found(5, c, range(index + 1, index + 1001)):
            keys_found += 1
            if keys_found == 64:
                print(index)
                break
    index += 1
                
                
