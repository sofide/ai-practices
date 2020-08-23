"""
Luego de que ambientalistas logren prohibir el uso de animales vivos para experimentos,
un grupo de científicos se encuentra con la necesidad de programar un robot que simule
el comportamiento de ratas de laboratorio dentro de laberintos. El robot debe poder
encontrar 3 “comidas” escondidas dentro, “ingerirlas”, y salir del laberinto al
finalizar su “alimentación”.

El laberinto, con la entrada y las comidas, es el que se ve en la figura.


------+-----+-----+-----+-----+-----+
|     |     |     |XXXXX|     |XXXXX|
------+-----+-----+-----+-----+-----+
|     |XXXXX|  C  |XXXXX|     |     |
------+-----+-----+-----+-----+-----+
|     |     |XXXXX|     |XXXXX|     |
------+-----+-----+-----+-----+-----+
|XXXXX|     |     |     |  C  |  E  |
------+-----+-----+-----+-----+-----+
|  C  |XXXXX|     |XXXXX|     |XXXXX|
------+-----+-----+-----+-----+-----+
|     |     |     |XXXXX|     |     |
------+-----+-----+-----+-----+-----+

E = Entrada
C = Comida
"""
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    iterative_limited_depth_first,
)
from simpleai.search.viewers import BaseViewer

from utils import print_grid

# a state is defined by a tuple of two values:
# - a tuple with the position of the rat
# - a tuple of tuples with the position of the food that it's still remaining
INITIAL_STATE = (
    (3, 5),  # Rat position
    ((1, 2), (3, 4), (4, 0)),  # food positions
)

GOAL_STATE = (
    (3, 5),
    (),
)

WALLS_POSTITIONS = (
    (0, 3), (0, 5),
    (1, 1), (1, 3),
    (2, 2), (2, 4),
    (3, 0),
    (4, 1), (4, 3), (4, 5),
    (5, 3),
)

ROWS = 6
COLUMNS = 6


class RatabotsProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE

    def actions(self, state):
        # an action is defined as the position to where the rat can move
        (row, column), _ = state
        movements = (
            (row - 1, column),  # move up
            (row + 1, column),  # move down
            (row, column - 1),  # move left
            (row, column + 1),  # move right
        )
        actions = [
            (r, c)
            for r, c in movements
            if (r, c) not in WALLS_POSTITIONS
            and 0 <= r < ROWS
            and 0 <= c < COLUMNS
        ]

        return actions

    def result(self, state, action):
        _, food_left = state

        food_left = tuple(food for food in food_left if food != action)

        return (action, food_left)

    def cost(self, state, action, state2):
        return 1

    def print_state_representation(self, state):
        rat, food = state
        elements_to_print = {
            "R": [rat],
            "C": food,
            "XXX": WALLS_POSTITIONS,
            "E": [(3, 5)]
        }
        print_grid(ROWS, COLUMNS, elements_to_print)


metodos = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for metodo_busqueda in metodos:
    print()
    print('=' * 50)

    print("corriendo:", metodo_busqueda.__name__)
    visor = BaseViewer()
    problem = RatabotsProblem(INITIAL_STATE)
    result = metodo_busqueda(problem, graph_search=True, viewer=visor)

    print('estado final:')
    print(result.state)

    print('-' * 50)

    print('estadísticas:')
    print('cantidad de acciones hasta la meta:', len(result.path()))
    print(visor.stats)

    draw_path = input("Do you want to draw the path? [y/N]")
    if draw_path.lower() == "y":
        for _, state in result.path():
            problem.print_state_representation(state)
            continue_printing = input("Print the next state [Y/n]")

            if continue_printing.lower() == "n":
                break
