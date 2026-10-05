from dataclasses import dataclass
from fractions import Fraction

from pyrsistent import PVector, pset, pvector


@dataclass
class LinearEquations:
    A: PVector[PVector[Fraction]]
    b: PVector[Fraction]

    def __str__(self):
        return "\n".join(
            "| "
            + str([f"{x.numerator}/{x.denominator}" for x in a])
            + " | "
            + str(b)
            + " | "
            for a, b in zip(self.A, self.b)
        )


def parse_equation(input_data: str) -> LinearEquations:
    """Create a system of linear equations from a line of joltage
    information."""
    fields = input_data.strip().split()
    buttons = [pset(eval(field.replace(")", ",)"))) for field in fields[1:-1]]
    joltages = pvector(eval(fields[-1].replace("{", "[").replace("}", "]")))
    max_presses = pvector(
        [min(joltages[c] for c in button) for button in buttons]
    )
    matrix = pvector()
    for i in range(len(joltages)):
        matrix = matrix.append(
            pvector(
                [
                    Fraction(1) if i in buttons[m] else Fraction(0)
                    for m in range(len(buttons))
                ]
            )
        )
    return LinearEquations(matrix, joltages)


def swap_rows(lineqs: LinearEquations, i: int, j: int) -> LinearEquations:
    return LinearEquations(
        lineqs.A.set(i, lineqs.A[j]).set(j, lineqs.A[i]),
        lineqs.b.set(i, lineqs.b[j]).set(j, lineqs.b[i]),
    )


def multiply_row(
    lineqs: LinearEquations, i: int, scalar: Fraction
) -> LinearEquations:
    return LinearEquations(
        lineqs.A.set(i, pvector(x * scalar for x in lineqs.A[i])),
        lineqs.b.set(i, lineqs.b[i] * scalar),
    )


def add_row(
    lineqs: LinearEquations, fro: int, to: int, scalar: Fraction
) -> LinearEquations:
    return LinearEquations(
        lineqs.A.set(
            to,
            pvector(
                x + y * scalar for x, y in zip(lineqs.A[to], lineqs.A[fro])
            ),
        ),
        lineqs.b.set(to, lineqs.b[to] + lineqs.b[fro] * scalar),
    )


def zero_pivot_column(lineqs: LinearEquations, pc: int):
    for i in range(pc + 1, len(lineqs.A)):
        lineqs = add_row(
            lineqs, pc, i, -Fraction(lineqs.A[i][pc], lineqs.A[pc][pc])
        )
    return lineqs


def find_next_pivot(lineqs: LinearEquations, row: int, col: int) -> int | None:
    for i in range(row, len(lineqs.A)):
        if lineqs.A[i][col] != 0:
            return i
    return None


def gaussian_elimination(lineqs: LinearEquations):
    row = 0
    for col in range(len(lineqs.A[0])):
        if (p := find_next_pivot(lineqs, row, col)) is not None:
            lineqs = swap_rows(lineqs, row, p)
            lineqs = multiply_row(lineqs, row, Fraction(1, lineqs.A[row][col]))
            for r in range(row + 1, len(lineqs.A)):
                lineqs = add_row(lineqs, row, r, -lineqs.A[r][col])
            row += 1
    return lineqs


def is_row_echelon(lineqs: LinearEquations) -> bool:
    for r in range(1, len(lineqs.A)):
        for c in range(min(r, len(lineqs.A[0]))):
            if lineqs.A[r][c] != 0:
                return False
    return True


max_unknowns = 0
for i, line in enumerate(open("input", "r").readlines()):
    lineqs = parse_equation(line)
    print(i)
    nrows = len(lineqs.A)
    ncols = len(lineqs.A[0])
    unknowns = ncols - nrows
    max_unknowns = max(max_unknowns, unknowns)
    print(f"{nrows} rows, {ncols} columns, {unknowns} unknowns")
    print(lineqs)
    print()
    print(gaussian_elimination(lineqs))
    print()
    print()
print(f"{max_unknowns = }")
