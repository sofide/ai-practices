"""
Se desea resolver el siguiente problema: dado el mismo tablero de 7x7, llenar el tablero
de reyes y soldados, pero respetando las siguientes condiciones: un rey nunca puede
tener más de 1 (otro) rey en sus casillas adyacentes, y la cantidad total de soldados
debe mayor que la cantidad de reyes, pero menor al doble de la cantidad total de reyes
(ej: si hay 10 reyes, puede haber 15 soldados , pero no 5 soldados, 20 soldados, ni 30
soldados).
"""
from itertools import combinations
from collections import defaultdict

from simpleai.search import (
    CspProblem,
    backtrack,
    convert_to_binary,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from simpleai.search.csp import convert_to_binary

from utils import print_grid

BOARD_SIZE = 7

VARIABLES = [
    (row, column)
    for row in range(BOARD_SIZE)
    for column in range(BOARD_SIZE)
]

KING = "king"
SOLDIER = "soldier"

DOMAINS = {
    variable: [KING, SOLDIER]
    for variable in VARIABLES
}

CONSTRAINTS = []

def no_king_adjacent(variables, values):
    if values == (KING, KING):
        (a_row, a_column), (b_row, b_column) = variables
        ham_distance = abs(a_row - b_row) + abs(a_column - b_column)
        return ham_distance > 1

    return True

for variables_pair in combinations(VARIABLES, 2):
    CONSTRAINTS.append((variables_pair, no_king_adjacent))


def soldiers_and_king_quantity(variables, values):
    kings_qty = values.count(KING)
    soldiers_qty = values.count(SOLDIER)

    return kings_qty < soldiers_qty < kings_qty * 2

CONSTRAINTS.append((VARIABLES, soldiers_and_king_quantity))

def print_result(result):
    elements = defaultdict(list)
    for position, person in result.items():
        elements[person].append(position)

    print_grid(BOARD_SIZE, BOARD_SIZE, elements,   9)
    values = list(result.values())
    kings_qty = values.count(KING)
    soldiers_qty = values.count(SOLDIER)

    print("Total kings:", kings_qty)
    print("Total soldiers:", soldiers_qty)


if __name__ == "__main__":
    problem = CspProblem(VARIABLES, DOMAINS, CONSTRAINTS)

    print("MIN CONFLICTS")
    result = min_conflicts(problem, iterations_limit=100)

    print_result(result)

    print("-"* 50)
    print("BACKTRACKING")
    result = backtrack(problem)
    print_result(result)



