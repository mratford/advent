from functools import cache
from copy import deepcopy


RESOURCES = ["ore", "clay", "obsidian"]


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


def new_resources():
    return {
        "ore": 0,
        "clay": 0,
        "obsidian": 0,
        "bots": {"ore": 1, "clay": 0, "obsidian": 0},
    }


def update_resources(blueprint, resources, built_bot):
    r = deepcopy(resources)
    for req in blueprint[built_bot]:
        r.update({req: resources[req] - blueprint[built_bot][req]})
    return r


def mine_resources(resources):
    r = deepcopy(resources)
    for resource in RESOURCES:
        r[resource] += r["bots"][resource]
    return r


def enough_resources(blueprint, resources, bot_to_build):
    return all(blueprint[bot_to_build].get(r, 0) <= resources[r] for r in RESOURCES)


def opt_geodes(blueprint, resources=new_resources(), time=24):
    # Try a DFS as caching takes all the memory
    stack = [(0, resources, time)]
    max_geodes = 0

    max_needed = {
        resource: max(blueprint[bot].get(resource, 0) for bot in blueprint)
        for resource in RESOURCES
    }

    while stack:
        geodes, resources, time_left = stack.pop()

        if time_left == 0:
            max_geodes = max(geodes, max_geodes)
        # If there are enough resources for a geode robot build it
        elif enough_resources(blueprint, resources, "geode"):
            r = update_resources(blueprint, resources, "geode")
            stack.append((time_left - 1 + geodes, mine_resources(r), time_left - 1))
        else:
            for bot in RESOURCES:
                if resources["bots"][bot] < max_needed[bot] and enough_resources(
                    blueprint, resources, bot
                ):
                    r = update_resources(blueprint, resources, bot)
                    stack.append((geodes, mine_resources(r), time_left - 1))
            # Is there enough time to build a bot and get resources from it?
            if time_left > 1:
                stack.append((geodes, mine_resources(resources), time_left - 1))
            else:
                max_geodes = max(geodes, max_geodes)

    return max_geodes


def part_1(blueprints):
    return sum(i * opt_geodes(blueprints[i]) for i in blueprints)


if __name__ == "__main__":
    data = parse_data(open("test_input").read())
    print("Part 1:", part_1(data))
