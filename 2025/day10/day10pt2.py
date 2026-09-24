from dataclasses import dataclass
from fractions import Fraction

from pyrsistent import PVector, pset, pvector


@dataclass
class LinearEquations:
    A: PVector[PVector[Fraction]]
    b: PVector[Fraction]


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
