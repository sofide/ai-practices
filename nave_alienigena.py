"""
Una nave alienígena se ha estrellado en la Tierra, y un grupo de investigadores desea
abrir su escotilla principal. Pero la misma posee un mecanismo bastante extraño, que
consta de una serie de botones que deben ser presionados en orden para lograr una
combinación de números en una pantalla.

La pantalla posee 3 casillas alineadas una al lado de la otra, cada una con un número
dentro. Inicialmente todas poseen el número cero. Los botones que pueden presionarse son
los siguientes:
- Botón rojo: Suma 3 al casillero inicial.
- Botón verde: Resta 2 al casillero inicial.
- Botón amarillo: Intercambia los valores de las dos primeras casillas.
- Botón celeste: Intercambia los valores de las dos últimas primeras casillas.

La secuencia de números que se debe lograr para abrir la escotilla es la siguiente:
5, 1, 8

- Plantee formalmente como problema de búsqueda tradicional, con código y comentarios
explicativos.
-  Plantee una heurística para el mismo. No hace falta que sea muy precisa, pero debe
ser admisible.
- Realice al menos 5 iteraciones de búsqueda A*. Por cada iteración especifique la
frontera con el valor de f asociado a cada nodo, y el nodo elegido.
"""
from collections import defaultdict

from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    astar,
    greedy,
    iterative_limited_depth_first,
)

from utils import print_grid, try_search_method

INITIAL_STATE = (0, 0, 0)
GOAL_STATE = (5, 1, 8)

RED = "red"
GREEN = "green"
YELLOW = "yellow"
BLUE = "blue"


class NaveAlienigena(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE

    def actions(self, state):
        return [RED, GREEN, YELLOW, BLUE]

    def result(self, state, action):
        first, second, third = state

        if action == RED:
            first += 3

        elif action == GREEN:
            first -= 2

        elif action == YELLOW:
            second, first = first, second

        elif action == BLUE:
            third, second = second, third

        return first, second, third

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        cost = 0
        for position, number in enumerate(GOAL_STATE):
            if state[position] != number:
                if number in state:
                    # estimate cost of 0.5 for having to swap because it can fix two
                    # digits in one movement.
                    cost += 0.5
                else:
                    # if the exact number is not in state at least one extra action is
                    # needed to create that number
                    cost += 1
                    a_red_button_of_distance = state[0] + 3 == number
                    a_green_button_of_distance = state[0] - 2 == number

                    if not a_red_button_of_distance and not a_green_button_of_distance:
                        # If the number is not at a red button or a green button of
                        # distance from any digit, at least another action will be neded
                        # to create the number
                        cost += 1

                    # cost of moving the created digit from 0 to expected position
                    # (cost will be 0.5 because a swap can fix two digits at once)
                    cost += position * 0.5

        return cost

    def print_state_representation(self, state):
        elements = defaultdict(list)
        for position, digit in enumerate(state):
            elements[str(digit)].append((0, position))

        print("the elements are:", elements)
        print("the state is:", state)
        print_grid(1, 3, elements)


methods = (
    # breadth_first,
    # depth_first,
    # iterative_limited_depth_first,
    # uniform_cost,
    greedy,
    astar,
)

for search_method in methods:
    try_search_method(search_method, NaveAlienigena, INITIAL_STATE)



"""
Iteraciones con astar:

GOAL_STATE = (5, 1, 8)


STATE REFERENCES:
+----+-------------+-----------------+-----------------------------+------------------+
|    | STATE       | ACUMULATED COST | HEURISTIC                   | ACUM + ESTIMATED |
|    |             |                 |n0+3|n0-2 | CALC       | COST|                  |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N1 | (0, 0, 0)   |    0            | 3  | -2  | (2+2.5+3)  | 7.5 |     7.5          |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N2 | (3, 0, 0)   |    1            | 6  | 1   |  2+1.5+3   | 6.5 |     7.5          |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N3 | (-2, 0, 0)  |    1            | 1  |  -4 |  2+1.5+3   | 6.5 |     7.5          |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N4 | (1, 0, 0)   |    2            | 4  | -1  |  2+0.5+3   | 5.5 |     7.5          |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N5 | (-4, 0, 0)  |    2            | -1 | -6  |  2+2.5+3   | 7.5 |     9.5          |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N6 | (0, -2, 0)  |    2            |  3 |  -2 |  2+2.5+3   | 7.5 |      9.5         |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N7 | (4, 0, 0)   |    3            | 7  |  2  |  2+2.5+3   | 7.5 |     10.5         |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N8 | (-1, 0, 0)  |    3            | 2  |  -3 |  2+2.5+3   | 7.5 |     10.5         |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N9 | (0, 1, 0)   |    3            | 3  |  -2 |  2+3       |  5  |      8           |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N10| (6, 0, 0)   |    2            | 9  |  4  |  2+2.5+3   | 7.5 |     9.5          |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N11| (1, 0, 0)   |    2            |    SAME STATE AND AC COST AS N4                |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N12| (0, 3, 0)   |    2            | 3  | -2  |  2+2.5+3   | 7.5 |     9.5          |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N13| (3, 1, 0)   |    4            | 6  |  1  |  2+3       |  5  |     9            |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N14| (-2, 1, 0)  |    4            | 1  |  -4 |  2+3       |  5  |     9            |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N15| (1, 0, 0)   |    4            |    SAME STATE AND GRATER AC COST THAN N4       |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N16| (0, 0, 1)   |    4            | 3  | -2  |  2+0.5+3   | 5.5 |     9.5          |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N17| (6, 1, 0)   |    5            | 9  |  4  |  2+3       |  5  |     10           |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N18| (1, 1, 0)   |    5            | 4  |  -1 |  2+3       |  5  |     10           |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N19| (1, 3, 0)   |    5            | 4  |  -1 |  2+0.5+3   | 5.5 |     10.5         |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
| N20| (3, 0, 1)   |    5            | 6  |  1  |  2+0.5+3   | 5.5 |                  |
+----+-------------+-----------------+----+-----+------------+-----+------------------+
N1: (0, 0, 0)

+---------------------------+----------------+---------+-------------------------------+
| FRIDGE                    | SELECTED STATE | IS GOAL |  CHILDREN                     |
+---------------------------+----------------+---------+-------------------------------+
|                           |  N1            |   NO    | N2 N3                         |
+---------------------------+----------------+---------+-------------------------------+
| N2                        |  N3            |   NO    | N4 N5 N6                      |
+---------------------------+----------------+---------+-------------------------------+
| N2 N5 N6                  |  N4            |   NO    | N7 N8 N9                      |
+---------------------------+----------------+---------+-------------------------------+
| N9 N5 N6 N7 N8            |  N2            |   NO    | N10 N12                       |
+---------------------------+----------------+---------+-------------------------------+
| N10 N12 N5 N6 N7 N8       |  N9            |   NO    | N13 N14 N16                   |
+---------------------------+----------------+---------+-------------------------------+
| N14 N16 N10 N12 N5 N7 N8  |  N13           |   NO    | N17 N18 N19 N20               |
+---------------------------+----------------+---------+-------------------------------+





"""
