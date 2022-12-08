def parse_data(s):
    return [[int(c) for c in row] for row in s.strip().splitlines()]


def part_1(data):
    total = 0
    for r_i, row in enumerate(data):
        for c_i, tree in enumerate(data[r_i]):
            if (
                all(x < tree for x in row[:c_i])
                or all(x < tree for x in row[c_i + 1 :])
                or all(x < tree for x in (d[c_i] for d in data[:r_i]))
                or all(x < tree for x in (d[c_i] for d in data[r_i + 1 :]))
            ):
                total += 1
    return total


def takewhile_plus_one(p, i):
    for x in iter(i):
        yield x
        if not p(x):
            break


def part_2(data):
    max_score = 0
    # Only take the inner trees as the border ones will always be zero and they
    # mess up the indexing
    for r_i, row in list(enumerate(data))[1:-1]:
        for c_i, tree in list(enumerate(data[r_i]))[1:-1]:
            f = lambda x: x < tree
            visible_west = len(list(takewhile_plus_one(f, data[r_i][c_i - 1 :: -1])))
            visible_east = len(list(takewhile_plus_one(f, data[r_i][c_i + 1 :])))
            visible_north = len(
                list(takewhile_plus_one(f, (d[c_i] for d in data[r_i - 1 :: -1])))
            )
            visible_south = len(
                list(takewhile_plus_one(f, (d[c_i] for d in data[r_i + 1 :])))
            )
            scenic_score = visible_west * visible_east * visible_north * visible_south
            max_score = max(max_score, scenic_score)
    return max_score


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))
