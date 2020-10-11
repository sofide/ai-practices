"""
Robots defensivos secretos. (continúa…)

Luego del último ataque, se decidió incrementar el número de robots a 6, y ya no
permanecerán almacenados, sino que se ubicarán en posiciones defensivas fijas y
permanentes.

Pero deben respetarse algunas restricciones:

- No puede haber dos robots en la misma habitación, generarían demasiadas molestias para
los científicos.
- No puede haber dos robots en habitaciones adyacentes, impedirían demasiado la
circulación.
- Las habitaciones restringidas siguen sin poder contener robots.
- Las dos habitaciones que poseen puertas al exterior deben contener un robot.
------+-----+-----+-----+-----+
|     |     |  X  |     |  P  |
------+-----+-----+-----+-----+
|     |     |     |  X  |     |
------+-----+-----+-----+-----+
|     |  X  |     |     |     |
------+-----+-----+-----+-----+
|     |     |  P  |     |     |
------+-----+-----+-----+-----+

X: Habitación no accesible por los Robots
P: Ubicación de las puertas
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

ROWS = 4
COLUMNS = 5

RESTRICTED_AREAS = [(0, 2), (1, 3), (2, 1)]

DOORS = [(0, 4), (3, 2)]

VARIABLES = [f"R{x}" for x in range(6)]

ALL_ROOMS = [
    (row, column)
    for row in range(ROWS)
    for column in range(COLUMNS)
]
NON_RESTRICTED_ROOMS = [room for room in ALL_ROOMS if room not in RESTRICTED_AREAS]

DOMAINS = {robot: NON_RESTRICTED_ROOMS for robot in VARIABLES}

CONSTRAINTS = []


def no_adjacent_nor_same_room(variables, values):
    (row_robot_a, column_robot_a), (row_robot_b, column_robot_b) = values
    manhattan_distance = (
        abs(row_robot_a - row_robot_b)
        + abs(column_robot_a - column_robot_b)
    )
    return manhattan_distance > 1


for two_variables in combinations(VARIABLES, 2):
    CONSTRAINTS.append((two_variables, no_adjacent_nor_same_room))


def robots_in_door(variables, values):
    for door in DOORS:
        if not door in values:
            return False

    return True

CONSTRAINTS.append((VARIABLES, robots_in_door))

def print_result(result):
    elements = {
        "D": DOORS,
        "X": RESTRICTED_AREAS,
    }
    for robot, position in result.items():
        elements[robot] = [position]

    print_grid(ROWS, COLUMNS, elements)

if __name__ == "__main__":
    problem = CspProblem(VARIABLES, DOMAINS, CONSTRAINTS)

    print("MIN CONFLICTS")
    result = min_conflicts(problem, iterations_limit=100)

    print_result(result)

    print("-"* 50)
    print("BACKTRACKING")
    result = backtrack(problem)
    print_result(result)
