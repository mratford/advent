from fractions import Fraction

from day10pt2 import LinearEquations, parse_equation
from pyrsistent import pvector


def test_parsing():
    line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    expected_matrix = pvector(
        pvector([Fraction(x) for x in row])
        for row in [
            [0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0],
            [1, 1, 0, 1, 0, 0],
        ]
    )
    expected_joltages = pvector([3, 5, 4, 7])
    assert parse_equation(line) == LinearEquations(
        expected_matrix, expected_joltages
    )
