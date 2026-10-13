from fractions import Fraction

import pytest
from day10pt2 import (
    LinearEquations,
    add_row,
    all_possible,
    expand_to_square,
    find_next_pivot,
    gaussian_elimination,
    max_possible,
    multiply_row,
    parse_equation,
    solve,
    solve_row_echelon,
    swap_cols,
    swap_rows,
    zero_pivot_column,
)
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


def test_swap_cols(leqs1):
    expected = create_linear_equations(
        [[1, 3, 2], [4, 6, 5], [7, 9, 8]], [10, 12, 11]
    )
    assert swap_cols(leqs1, 1, 2) == expected


def test_multiply(leqs1):
    expected = create_linear_equations(
        [[1, 2, 3], [8, 10, 12], [7, 8, 9]], [10, 22, 12]
    )
    assert multiply_row(leqs1, 1, 2) == expected


def test_add(leqs1):
    expected = create_linear_equations(
        [[1, 2, 3], [6, 9, 12], [7, 8, 9]], [10, 31, 12]
    )
    assert add_row(leqs1, 0, 1, 2) == expected


def test_zero_pivot_column():
    leqs = create_linear_equations(
        [[2, 1, 0], [1, 0, 1], [0, 1, 1]], [4, 3, 1]
    )
    expected = create_linear_equations(
        [[2, 1, 0], [0, Fraction(-1, 2), 1], [0, 1, 1]], [4, 1, 1]
    )
    assert zero_pivot_column(leqs, 0) == expected


def test_find_next_pivot():
    leqs = create_linear_equations(
        [[1, 0, 1, 0], [0, 0, 0, 1], [0, 0, 3, 7], [0, 0, 54, 74231]],
        [1, 4545, 457, 6913],
    )
    assert find_next_pivot(leqs, 1, 1) is None
    assert find_next_pivot(leqs, 1, 2) == 2


def test_gaussian_elimination():
    leqs = create_linear_equations(
        [[1, 2, 3], [2, 1, 0], [3, 0, 2]], [14, 4, 9]
    )
    expected = create_linear_equations(
        [[1, 2, 3], [0, 1, 2], [0, 0, 1]], [14, 8, 3]
    )
    assert gaussian_elimination(leqs) == expected


def test_solve_row_echelon():
    leqs = create_linear_equations(
        [[1, 2, 3], [0, 1, 2], [0, 0, 1]], [14, 8, 3]
    )
    expected = pvector([1, 2, 3])
    assert solve_row_echelon(leqs) == expected


def test_expand_to_square():
    leqs = create_linear_equations(
        [
            [1, 2, 3, 4],
            [0, 1, 5, 6],
        ],
        [7, 8],
    )
    expected = create_linear_equations(
        [[1, 2, 3, 4], [0, 1, 5, 6], [0, 0, 1, 0], [0, 0, 0, 1]], [7, 8, 0, 0]
    )
    assert expand_to_square(leqs) == expected


def test_max_possible():
    leqs = create_linear_equations(
        [[1, 1, 1, 1], [1, 0, 0, 1], [1, 1, 0, 0]], [5, 6, 4]
    )
    assert max_possible(leqs, 3) == 5


def test_all_possible():
    leqs = create_linear_equations(
        [[1, 1, 1, 1], [1, 0, 0, 1], [1, 1, 0, 0]], [2, 6, 4]
    )
    assert list(all_possible(leqs, 3)) == [(3, 0), (3, 1), (3, 2)]


def test_solve():
    assert solve("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}") == 10


def test_solve_2():
    assert (
        solve("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}")
        == 12
    )


def test_solve_3():
    assert (
        solve(
            "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        )
        == 11
    )
