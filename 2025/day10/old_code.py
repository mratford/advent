from collections import Counter, namedtuple
from itertools import chain, combinations, permutations
from pyrsistent import pmap, pvector, pset, PSet
from functools import reduce
from dataclasses import dataclass

@dataclass
class Equation:
    joltage: int 
    buttons: PSet

    def __str__(self):
        return f"{self.joltage} = {' + '.join('n' + str(b) for b in self.buttons)}"

def create_eqs(buttons, joltages):
    eqs = pvector()
    for i, joltage in enumerate(joltages):
        bs = pset({bi for bi, b in enumerate(buttons) if i in b})
        eqs = eqs.append(Equation(joltage, bs))
    ns = pmap()
    return eqs, ns


def simplify_step(eqs, ns):
    if any(
        eq.joltage < 0 or (eq.joltage >= 0 and len(eq.buttons) == 0)
        for eq in eqs
    ):
        raise ValueError
    # Remove empty equation
    for i, eq in enumerate(eqs):
        if len(eq.buttons) == 0:
            eqs = eqs.delete[i]
            return True, eqs, ns
    # Remove duplicate equations
    for i, j in combinations(range(len(eqs)), 2):
        if eqs[i] == eqs[j]:
            # print(f"Removing duplicate: {eqs[j]}")
            eqs = eqs.delete(j)
            return True, eqs, ns
    # Resolve equations with single variable
    for i, eq in enumerate(eqs):
        if len(eq.buttons) == 1:
            # print(f"Resolved: {eqs[i]}")
            x = next(iter(eq.buttons))
            ns = ns.set(x, eq.joltage)
            eqs = eqs.delete(i)
            for i in range(len(eqs)):
                if x in eqs[i].buttons:
                    eqs[i].buttons = eqs[i].buttons.remove(x)
                    eqs[i].joltage = eqs[i].joltage - ns[x]
            return True, eqs, ns
    # If a joltage is zero, set all to zero
    for i, eq in enumerate(eqs):
        if eq.joltage == 0:
            # print(f"All zero: {eqs[i]}")
            for b in eq.buttons:
                eqs.append(Equation(0, pset({b})))
            eqs = eqs.delete(i)
            return True, eqs, ns
    # Resolve pairs of equations where one has an extra variable
    for i, j in permutations(range(len(eqs)), 2):
        if eqs[j].buttons - eqs[i].buttons == pset():
            diff = eqs[i].buttons - eqs[j].buttons
            if len(diff) == 1:
                x = next(iter(diff))
                xjolt = eqs[i].joltage - eqs[j].joltage
                # print(f"Worked out: {eqs[i]} - {eqs[j]}")
                eqs = eqs.append(Equation(xjolt, pset({x})))
                return True, eqs, ns
            else: 
                # print(f"Diffing: {eqs[i]} - {eqs[j]}")
                eqs = eqs.append(Equation(eqs[i].joltage - eqs[j].joltage, diff))
                eqs = eqs.delete(i)
                return True, eqs, ns
    # If a variable is in all equations set it to the minimum joltage
    if len(eqs) > 1:
        in_all = list(reduce(
            lambda x, y: x.intersection(y), 
            (eq.buttons for eq in eqs)
        ))
        if in_all:
            i = in_all[0]
            min_joltage = min(eq.joltage for eq in eqs)
            # print(f"All equations contain {i}, setting to {min_joltage}")
            eqs = eqs.append(Equation(min_joltage, pset({i})))
            return True, eqs, ns
    return (False, eqs, ns)
        
    while simplify():
        pass

def simplify_eqs(eqs, ns):
    simplifying = True
    while simplifying:
        simplifying, eqs, ns = simplify_step(eqs, ns)
    return eqs, ns
        

_, bs, js = test_data[1]
eqs, ns = create_eqs(bs, js)
simplify_eqs(eqs, ns)

from fractions import Fraction
from copy import deepcopy

def create_eqs(buttons, joltages):
    matrix = []
    nb = len(buttons)
    for i, joltage in enumerate(joltages):
        matrix.append(
            [
                1 if i in buttons[j] else 0
                for j in range(len(buttons))
            ] + [joltage]
        )
    return matrix

def gaussian_elimination(matrix):
    w = len(matrix[0]) - 1
    h = len(matrix)
    d = min(w, h)
    max_joltage = {
        u: min((matrix[i][-1] for i in range(h) if matrix[i][u] != 0), default=0)
        for u in range(w)
    }
    for i in range(d):
        # print_matrix(matrix)
        pivot_row = i
        while pivot_row < d - 1 and matrix[pivot_row][i] == 0:
            pivot_row += 1
        # print(f"{pivot_row = }")
        if pivot_row < h:
            if i != pivot_row:
                tmp = deepcopy(matrix[i])
                matrix[i] = matrix[pivot_row]
                matrix[pivot_row] = tmp
            pivot = matrix[i][i]
            if pivot == 0:
                pivot_col = i
                while pivot_col < w and matrix[i][pivot_col] == 0:
                    pivot_col += 1
                if pivot_col < w:
                    tmp = [row[i] for row in matrix]
                    for r in range(len(matrix)):
                        matrix[r][i] = matrix[r][pivot_col]
                        matrix[r][pivot_col] = tmp[r]
                    pivot = matrix[i][i]
                    tmp = max_joltage[i]
                    max_joltage[i] = max_joltage[pivot_col]
                    max_joltage[pivot_col] = tmp
            # print(f"{pivot = }")
            if pivot != 0:
                matrix[i] = [Fraction(x, pivot) for x in matrix[i]]
                # print("---")
                # print(matrix[i])
                for j in range(i + 1, h):
                    # print(j)
                    # print(matrix[j])
                    matrix[j] = [x - matrix[j][i] * matrix[i][k] for k, x in enumerate(matrix[j])]
                    # print(matrix[j])

    return matrix[:d], max_joltage

def print_matrix(m):
    print("---")
    for r in m:
        print([x.numerator if x.is_integer() else x for x in r])
    print("---")
    
import math
import itertools

def calculate_presses(matrix):
    ns = {}
    for i in range(len(matrix) - 1, -1, -1):
        row = matrix[i]
        ns[i] = row[-1] - sum(ns[j] * row[j] for j in range(i + 1, len(matrix[0]) - 1))
    if all(n >= 0 and n.is_integer() for n in ns.values()):
        return sum(ns.values())
    else:
        return math.inf

def prepare_for_gauss(eqs):
    to_resolve = set()
    for eq in eqs:
        to_resolve |= set(eq.buttons)
    max_joltage = {
        b: max(eq.joltage for eq in eqs if b in eq.buttons)
        for b in to_resolve
    }
    trans = dict(enumerate(sorted(to_resolve, key=lambda x: max_joltage[x], reversed=True)))
    matrix = []
    for eq in eqs:
        matrix.append([1 if trans[i] in eq.buttons else 0 for i in trans] + [eq.joltage])


def min_presses(buttons, joltages):
    # eqs, ns = create_eqs(buttons, joltages)
    # eqs, resolved_ns = simplify_eqs(eqs, ns)
    # to_resolve = set()
    # for eq in eqs:
    #     to_resolve |= set(eq.buttons)
    # if len(to_resolve) == 0:
    #     return sum(resolved_ns.values())
    # trans = dict(enumerate(sorted(to_resolve)))
    # matrix = []
    # for eq in eqs:
    #     matrix.append([1 if trans[i] in eq.buttons else 0 for i in trans] + [eq.joltage])
    matrix = create_eqs(buttons, joltages)
    # print_matrix(matrix)
    matrix, max_joltage = gaussian_elimination(matrix)
    n_variables = len(matrix[0]) - 1
    n_equations = len(matrix)
    n_unknowns = n_variables - n_equations 
    # print_matrix(matrix)
    presses = {}
    for _ in range(n_unknowns):
        matrix.append([Fraction(0, 1)] * (n_variables + 1))
    unknowns = [i for i, r in enumerate(matrix) if all(x == 0 for x in r)]
    for u in unknowns:
        matrix[u][u] = 1
    # print_matrix(matrix)
    print(f"{len(unknowns)} unknowns")
    min_so_far = math.inf
    combos = math.prod(int(max_joltage[u]) + 1 for u in unknowns)
    print(f"{combos} combinations")
    # print(f"{max_joltage =}")
    for xs in itertools.product(*[range(int(max_joltage[u]) + 1) for u in unknowns]):
        # print(xs)
        for i, n in zip(unknowns, xs):
            matrix[i][-1] = n
        # print_matrix(matrix)
        presses = calculate_presses(matrix)
        # print(presses)
        min_so_far = min(min_so_far, calculate_presses(matrix))
        
    return min_so_far #+ sum(resolved_ns.values())
