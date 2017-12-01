def supports_tls(address):
    tls = False
    while len(address) > 0:
        if address[0] == '[':
            address = address[1:]
            p = address.find(']')
            if has_abba(address[:p]):
                return False
            address = address[p + 1:]
        else:
            p = address.find('[')
            if p == -1:
                p = len(address)
            tls = tls or has_abba(address[:p])
            address = address[p:]
    return tls


def has_abba(s):
    for i in range(len(s) - 3):
        if s[i] == s[i + 3] and s[i + 1] == s[i + 2] and s[i] != s[i + 1]:
            return True
    return False


count = 0

with open('input', 'rt') as f:
    for line in [l.strip() for l in f]:
        if supports_tls(line):
            count += 1

print(count)
