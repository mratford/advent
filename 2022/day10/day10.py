STARTING_VALUE = 1


def parse_data(s):
    return s.strip().splitlines()


def do_instruction(instruction, register):
    if instruction.startswith("noop"):
        yield register
    else:  # addx
        yield register
        yield register + int(instruction.split()[1])


def find_cycles(instructions):
    cycles = []
    X = STARTING_VALUE
    for i in instructions:
        for r in do_instruction(i, X):
            cycles.append(r)
            X = r
    return cycles


def signal_strength_during_cycle(cycles, n):
    if n == 1:
        return 1
    no_of_cycles = len(cycles)
    no_of_complete_runs, pos_in_incomplete_run = divmod(n - 1, no_of_cycles)
    return n * (
        (cycles[-1] - STARTING_VALUE) * no_of_complete_runs
        + (
            cycles[pos_in_incomplete_run - 1]
            if pos_in_incomplete_run > 0
            else STARTING_VALUE
        )
    )


def part_1(instructions):
    cycles = find_cycles(instructions)
    cycles_of_interest = [20, 60, 100, 140, 180, 220]
    return sum(signal_strength_during_cycle(cycles, n) for n in cycles_of_interest)


def part_2(instructions):
    crt = ""
    cycles = find_cycles(instructions)
    for i in range(0, 240, 40):
        for cycle in range(i, i + 40):
            crt += (
                "#"
                if abs(
                    (cycles[cycle - 1] if cycle > 0 else STARTING_VALUE) - (cycle - i)
                )
                <= 1
                else "."
            )
        crt += "\n"
    return crt


if __name__ == "__main__":
    instructions = parse_data(open("input").read())
    cycles = find_cycles(instructions)
    print("Part 1:", part_1(instructions))
    print(f"Part 2:\n{part_2(instructions)}")
