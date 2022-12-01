cals = eval(
    "[" + open("input").read().strip().replace("\n\n", ",").replace("\n", "+") + "]"
)
print(f"Part 1: {max(cals)}")
print(f"Part 2: {sum(sorted(cals)[-3:])}")
