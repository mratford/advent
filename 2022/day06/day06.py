text = open("input").read().strip()
print([next(i for i in range(n, len(text)) if len(set(text[i-n:i])) == n) for n in (4, 14)])
