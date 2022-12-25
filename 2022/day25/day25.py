from itertools import count

snafu = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def snafu_to_decimal(s):
    return sum(snafu[c] * x for c, x in zip(reversed(s), (5**i for i in count())))


def decimal_to_snafu(x):
    rev_snafu = []
    while True:
        x, r = divmod(x, 5)
        if r < 3:
            rev_snafu.append(str(r))
        else:
            x += 1
            rev_snafu.append("=" if r == 3 else "-")
        if x == 0:
            return "".join(reversed(rev_snafu))


data = open("input").read().strip().splitlines()
print(decimal_to_snafu(sum(snafu_to_decimal(snafu) for snafu in data)))
