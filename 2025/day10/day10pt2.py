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
