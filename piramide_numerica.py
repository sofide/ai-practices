"""
Pirámide numérica

Dada la pirámide de números de la imagen, se desea rellenar los casilleros utilizando
números del 1 al 50, de forma tal que cada casillero tenga el valor resultante de la
suma de sus dos casilleros inferiores, y que no haya dos casilleros con el mismo número.

         +----+
         | 48 |
      +----+----+
      |    |    |
   +----+----+----+
   |    |    |    |
+----+----+----+----+
| 5  |  8 |    |  3 |
+----+----+----+----+
"""
from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from simpleai.search.csp import convert_to_binary

from utils import print_grid


VARIABLES = [
    "00",
    "10", "11",
    "20", "21", "22",
    "30", "31", "32", "33"
]

DOMAINS = {
    variable: list(range(1, 51))
    for variable in VARIABLES
}

DOMAINS["00"] = [48]
DOMAINS["30"] = [5]
DOMAINS["31"] = [8]
DOMAINS["33"] = [3]

CONSTRAINTS = []

def differents(variables, values):
    box_a, box_b = values
    return box_a != box_b


for variables_pair in combinations(VARIABLES, 2):
    CONSTRAINTS.append((variables_pair, differents))


def box_sum(variables, values):
    box_top, box_bottom_a, box_bottom_b = values

    return box_top == box_bottom_a + box_bottom_b

CONSTRAINTS.append((("00", "10", "11"), box_sum))
CONSTRAINTS.append((("10", "20", "21"), box_sum))
CONSTRAINTS.append((("11", "21", "22"), box_sum))
CONSTRAINTS.append((("20", "30", "11"), box_sum))
CONSTRAINTS.append((("21", "31", "32"), box_sum))
CONSTRAINTS.append((("22", "32", "33"), box_sum))

def print_result(result):
    elements = {}
    for position, value in result.items():
        row, column = position
        elements[str(value)] = [(int(row), int(column))]

    print_grid(4, 4, elements, 3)


if __name__ == "__main__":
    problem = CspProblem(VARIABLES, DOMAINS, CONSTRAINTS)

    print("MIN CONFLICTS")
    result = min_conflicts(problem, iterations_limit=100)

    print_result(result)

    print("-"* 50)
    print("BACKTRACKING")
    result = backtrack(problem)
    print_result(result)
