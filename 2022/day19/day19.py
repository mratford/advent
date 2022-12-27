from functools import cache
from copy import deepcopy
from functools import cache
from heapq import heappop, heappush
import math


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


class Resources:
    def __init__(self, time=24):
        self.time = time
        self.geodes = 0
        self.r = {
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "bots": {"ore": 1, "clay": 0, "obsidian": 0},
        }

    def build_robot(self, blueprint, bot):
        self.mine_resources()
        for req in blueprint[bot]:
            self.r[req] -= blueprint[bot][req]
        if bot != "geode":
            self.r["bots"][bot] += 1
        else:
            self.geodes += self.time
        return self

    def mine_resources(self):
        self.time -= 1
        for resource in RESOURCES:
            self.r[resource] += self.r["bots"][resource]
        return self

    def enough_resources(self, blueprint, bot_to_build):
        return all(
            blueprint[bot_to_build][resource] <= self.r[resource]
            for resource in blueprint[bot_to_build]
        )

    def __lt__(self, other):
        return (
            -self.geodes,
            -self.r["bots"]["obsidian"],
            -self.r["bots"]["clay"],
            -self.r["bots"]["ore"],
            -self.r["obsidian"],
            -self.r["clay"],
            -self.r["ore"],
            -self.time,
        ) < (
            -other.geodes,
            -other.r["bots"]["obsidian"],
            -other.r["bots"]["clay"],
            -other.r["bots"]["ore"],
            -other.r["obsidian"],
            -other.r["clay"],
            -other.r["ore"],
            -self.time,
        )


@cache
def max_geodes_in_time_left(t):
    return t * (t - 1) // 2


def opt_geodes(blueprint, time=24):
    # Try a priority search as caching takes all the memory
    resources = Resources(time)
    q = [resources]
    max_geodes = 0

    max_needed = {
        resource: max(blueprint[bot].get(resource, 0) for bot in blueprint)
        for resource in RESOURCES
    }

    while q:
        resources = heappop(q)
        max_geodes = max(resources.geodes, max_geodes)

        # Try to create each robot, prune if run out of time
        for bot in blueprint:
            if all(resources.r["bots"][resource] > 0 for resource in blueprint[bot]):
                r = deepcopy(resources)
                while not r.enough_resources(blueprint, bot):
                    r.mine_resources()
                if bot == "geode" and r.time >= 1:
                    heappush(q, r.build_robot(blueprint, "geode"))
                elif (
                    r.time >= 2
                    and r.geodes + max_geodes_in_time_left(r.time - 1) > max_geodes
                    and r.r["bots"][bot] < max_needed[bot]
                ):
                    heappush(q, r.build_robot(blueprint, bot))

    return max_geodes


def part_1(blueprints):
    return sum(i * opt_geodes(blueprints[i], time=24) for i in blueprints)


def part_2(blueprints):
    return math.prod(opt_geodes(blueprints[i], time=32) for i in [1, 2, 3])


if __name__ == "__main__":
    data = parse_data(open("input").read())
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))
