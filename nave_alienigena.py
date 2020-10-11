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
                # If spected number is not in position at least one action is needed to
                # move it (only for positions different from the first one because is
                # posible to generate a number there without moving.
                if position != 0:
                    cost += 1
                if not number in state:
                    # if the exact number is not in state at least one extra action is
                    # needed to create that number
                    cost += 1
                    a_red_button_of_distance = (number - 3) in state
                    a_green_button_of_distance = (number + 2) in state
                    if not a_red_button_of_distance and not a_green_button_of_distance:
                        # If the number is not at a red button or a green button of
                        # distance from any digit, at least another action will be neded
                        # to create the number
                        cost += 1

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
