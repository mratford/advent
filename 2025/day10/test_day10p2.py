from fractions import Fraction

import pytest
from day10pt2 import LinearEquations, multiply_row, parse_equation, swap_rows
from pyrsistent import pvector


def create_linear_equations(A: list[list[int]], b: list[int]):
    return LinearEquations(
        pvector(pvector([Fraction(x) for x in row]) for row in A), pvector(b)
    )


@pytest.fixture
def leqs1():
    return create_linear_equations(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [10, 11, 12]
    )


def test_parsing():
    line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    expected = create_linear_equations(
        [
            [0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0],
            [1, 1, 0, 1, 0, 0],
        ],
        [3, 5, 4, 7],
    )
    assert parse_equation(line) == expected


def test_swapping(leqs1):
    expected = create_linear_equations(
        [
            [7, 8, 9],
            [4, 5, 6],
            [1, 2, 3],
        ],
        [12, 11, 10],
    )
    assert swap_rows(leqs1, 0, 2) == expected


def test_multiply(leqs1):
    expected = create_linear_equations(
        [[1, 2, 3], [8, 10, 12], [7, 8, 9]], [10, 22, 12]
    )
    assert multiply_row(leqs1, 1, 2) == expected
