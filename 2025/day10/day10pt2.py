import itertools
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterator, Tuple

import tqdm
from pyrsistent import PVector, pset, pvector


@dataclass
class LinearEquations:
    A: PVector[PVector[Fraction]]
    b: PVector[Fraction]
    max_possible: PVector[int]

    @property
    def nrows(self):
        return len(self.A)

    @property
    def ncols(self):
        return len(self.A[0])

    def __str__(self):
        return (
            "\n".join(
                "| "
                + str([f"{x.numerator}/{x.denominator}" for x in a])
                + " | "
                + str(b)
                + " | "
                for a, b in zip(self.A, self.b)
            )
            + " ".join(str(x) for x in self.max_possible)
            + "\n"
        )


def parse_equation(input_data: str) -> LinearEquations:
    """Create a system of linear equations from a line of joltage
    information."""
    fields = input_data.strip().split()
    buttons = [pset(eval(field.replace(")", ",)"))) for field in fields[1:-1]]
    joltages = pvector(eval(fields[-1].replace("{", "[").replace("}", "]")))
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
    # Calculate the maximum number of times a button can be pushed from a
    # joltages configuration. It's assumed that all the values in lineqs.A are
    # either 1 or 0, as they will be when first initialised.

    max_possible = pvector(
        [
            int(
                min(
                    joltages[i]
                    for i in range(len(joltages))
                    if matrix[i][button] == 1
                )
            )
            for button in range(len(matrix[0]))
        ]
    )
    return LinearEquations(matrix, joltages, max_possible)


def swap_rows(lineqs: LinearEquations, i: int, j: int) -> LinearEquations:
    return LinearEquations(
        lineqs.A.set(i, lineqs.A[j]).set(j, lineqs.A[i]),
        lineqs.b.set(i, lineqs.b[j]).set(j, lineqs.b[i]),
        lineqs.max_possible,
    )


def swap_cols(lineqs: LinearEquations, i: int, j: int) -> LinearEquations:
    A = lineqs.A
    mp = lineqs.max_possible
    for r in range(lineqs.nrows):
        A = A.set(r, A[r].set(i, A[r][j]).set(j, A[r][i]))
    return LinearEquations(A, lineqs.b, mp.set(i, mp[j]).set(j, mp[i]))


def multiply_row(
    lineqs: LinearEquations, i: int, scalar: Fraction
) -> LinearEquations:
    return LinearEquations(
        lineqs.A.set(i, pvector(x * scalar for x in lineqs.A[i])),
        lineqs.b.set(i, lineqs.b[i] * scalar),
        lineqs.max_possible,
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
        lineqs.max_possible,
    )


def zero_pivot_column(lineqs: LinearEquations, pc: int):
    for i in range(pc + 1, lineqs.nrows):
        lineqs = add_row(
            lineqs, pc, i, -Fraction(lineqs.A[i][pc], lineqs.A[pc][pc])
        )
    return lineqs


def find_next_pivot(lineqs: LinearEquations, row: int, col: int) -> int | None:
    for i in range(row, lineqs.nrows):
        if lineqs.A[i][col] != 0:
            return i
    return None


def gaussian_elimination(lineqs: LinearEquations):
    row = 0
    for col in range(len(lineqs.A[0])):
        if (p := find_next_pivot(lineqs, row, col)) is not None:
            lineqs = swap_rows(lineqs, row, p)
            lineqs = multiply_row(lineqs, row, Fraction(1, lineqs.A[row][col]))
            for r in range(row + 1, lineqs.nrows):
                lineqs = add_row(lineqs, row, r, -lineqs.A[r][col])
            row += 1
    return lineqs


def is_row_echelon(lineqs: LinearEquations) -> bool:
    for r in range(1, lineqs.nrows):
        for c in range(min(r, lineqs.ncols)):
            if lineqs.A[r][c] != 0:
                return False
    return True


def next_or_none(it):
    try:
        return next(it)
    except StopIteration:
        return None


def delete_row(lineqs: LinearEquations, row: int) -> LinearEquations:
    return LinearEquations(
        lineqs.A.delete(row), lineqs.b.delete(row), lineqs.max_possible
    )


def fix_partial_pivot(lineqs: LinearEquations) -> LinearEquations:
    pivot = 0
    while pivot < min(lineqs.nrows, lineqs.ncols):
        if lineqs.A[pivot][pivot] == 0:
            swap_col = next_or_none(
                c
                for c in range(pivot + 1, lineqs.ncols)
                if lineqs.A[pivot][c] != 0
            )
            if swap_col is not None:
                lineqs = swap_cols(lineqs, pivot, swap_col)
            else:
                if lineqs.b[pivot] != 0:
                    raise ValueError(f"Unsolvable: {lineqs}")
                else:
                    lineqs = delete_row(lineqs, pivot)
                    pivot = pivot - 1
        pivot = pivot + 1
    while lineqs.nrows > lineqs.ncols:
        lineqs = delete_row(lineqs, lineqs.nrows - 1)

    return lineqs


def solve_row_echelon(lineqs: LinearEquations) -> PVector[Fraction]:
    solution = pvector([Fraction(0)] * len(lineqs.A[0]))
    for r in range(lineqs.nrows - 1, -1, -1):
        solution = solution.set(
            r,
            (
                lineqs.b[r]
                - sum(
                    solution[i] * lineqs.A[r][i]
                    for i in range(r + 1, lineqs.ncols)
                )
            )
            / lineqs.A[r][r],
        )
    return solution


def expand_to_square(lineqs: LinearEquations) -> LinearEquations:
    return LinearEquations(
        lineqs.A.extend(
            [
                pvector([Fraction(0)] * lineqs.ncols).set(r, Fraction(1))
                for r in range(lineqs.nrows, lineqs.ncols)
            ]
        ),
        lineqs.b.extend([Fraction(0)] * (lineqs.ncols - lineqs.nrows)),
        lineqs.max_possible,
    )


def all_possible(
    lineqs: LinearEquations, button: int
) -> Iterator[Tuple[int, int]]:
    for x in range(lineqs.max_possible[button] + 1):
        yield (button, x)


def all_combinations(
    lineqs: LinearEquations, buttons: list[int]
) -> Iterator[LinearEquations]:
    lineqs = expand_to_square(lineqs)
    for xs in itertools.product(
        *(all_possible(lineqs, button) for button in buttons)
    ):
        next_combination = lineqs.b
        for b, x in xs:
            next_combination = next_combination.set(b, Fraction(x))
        yield LinearEquations(lineqs.A, next_combination, lineqs.max_possible)


def fewest_presses(lineqs: LinearEquations):
    row_echelon = fix_partial_pivot(gaussian_elimination(lineqs))
    if row_echelon.nrows >= row_echelon.ncols:
        solution = solve_row_echelon(row_echelon)
        return sum(solution)
    fewest = math.inf
    buttons = list(range(row_echelon.nrows, row_echelon.ncols))
    for le in all_combinations(row_echelon, buttons):
        possible_solution = solve_row_echelon(le)
        if all(x >= 0 and int(x) == x for x in possible_solution):
            fewest = min(fewest, sum(possible_solution))
    return fewest


def solve(s: str):
    return fewest_presses(parse_equation(s))


if __name__ == "__main__":
    with open("input") as f:
        lines = f.readlines()
    answer = 0
    for line in tqdm.tqdm(lines):
        answer = answer + solve(line)
    print(answer)
