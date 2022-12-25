from functools import cache
from copy import deepcopy


def ints(s):
    return [
        int(x)
        for x in "".join(c if c.isdigit() or c == "-" else " " for c in s).split()
    ]


def parse_data(s):
    blueprints = {}
    for line in s.strip().splitlines():
        inp = ints(line)
        blueprints[inp[0]] = {
            "ore": {"ore": inp[1]},
            "clay": {"ore": inp[2]},
            "obsidian": {"ore": inp[3], "clay": inp[4]},
            "geode": {"ore": inp[5], "obsidian": inp[6]},
        }
    return blueprints


def opt_geodes(blueprint, resources={"bots": {"ore": 1}}, time=24):
    # Try a DFS as caching takes all the memory
    stack = [(0, resources, time)]
    max_geodes = 0

    while stack:
        geodes, resources, time_left = stack.pop()
        
        if time_left == 0:
            max_geodes = max(geodes, max_geodes)
        # If there are enough resources for a geode robot build it
        elif (
            blueprint["geode"]["ore"] <= resources["ore"]
            and blueprint["geode"]["obsidian"] <= resources["obsidian"]
        ):
            r = deepcopy(resources)
            r.update({"ore": resources["ore"] - blueprint["geode"]["ore"],
                      "obsidian": resources["obsidian"] - blueprint["geode"]["obsidian"]})
            stack.append(time_left - 1 + geodes, r, time_left - 1)
        else:
            


def part_1(blueprints):
    return sum(i * opt_geodes(blueprints[i]) for i in blueprints)


if __name__ == "__main__":
    data = parse_data(open("test_input").read())
    print("Part 1:", part_1(data))
