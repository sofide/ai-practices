"""
Hnefatafl es un antiguo juego vikingo similar al ajedrez, en el que un jugador tiene un
pequeño ejército con un rey que debe escapar, mientras el otro jugador tiene un ejército
de más fichas y su objetivo es capturar al rey antes de que escape.

En este problema vamos a resolver una versión super simplificada, en la que los soldados
se encuentran fijos (no se mueven), y el rey está solo intentando escapar sin ser
atacado.

En esta versión el tablero tiene dimensiones de 7x7, el rey comienza en el casillero
central, y los soldados se encuentran en las posiciones del diagrama “Posiciones
iniciales”. El jugador debe lograr que el rey llegue a cualquiera de los bordes del
tablero en la menor cantidad posible de movimientos, pero sin ser atacado por ninguno de
los soldados en ningún momento (incluso cuando llega al borde). Los soldados atacan
desde casillas adyacentes (no en diagonal). Nunca puede haber dos fichas en la misma
posición, y los movimientos solo son a casilleros adyacentes (arriba, abajo, izquierda
o derecha, no en diagonal, de a 1 casillero).

Posiciones iniciales:
------+-----+-----+-----+-----+-----+-----+
|  X  |  X  |     |     |  X  |     |     |
------+-----+-----+-----+-----+-----+-----+
|     |     |     |     |  X  |     |     |
------+-----+-----+-----+-----+-----+-----+   R = Rey
|  X  |     |     |     |     |     |     |   X = Soldados enemigos
------+-----+-----+-----+-----+-----+-----+
|     |  X  |     |  R  |     |     |  X  |
------+-----+-----+-----+-----+-----+-----+
|  X  |     |     |     |     |     |     |
------+-----+-----+-----+-----+-----+-----+
|     |     |     |     |     |     |     |
------+-----+-----+-----+-----+-----+-----+
|     |     |     |  X  |     |  X  |     |
------+-----+-----+-----+-----+-----+-----+
"""
from collections import defaultdict

from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    iterative_limited_depth_first,
)

from utils import print_grid, try_search_method

INITIAL_STATE = (3, 3)  # King position
ENEMIES = (
    (0, 0), (0, 1), (0, 4),
    (1, 4),
    (2, 0),
    (3, 1), (3, 6),
    (4, 0),
    (6, 3), (6, 5),
)

BOARD_SIZE = 7


class HnefataflProblem(SearchProblem):
    def is_goal(self, state):
        # For a board of 7x7 the goal states are the ones with column or row with 0 or 6
        last_row_and_column = BOARD_SIZE - 1
        return 0 in state or last_row_and_column in state

    def actions(self, state):
        def adjacent_positions(row, column):
            return [
                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1),
            ]

        def enemy_can_attack(row, column):
            for position in adjacent_positions(row, column):
                if position in ENEMIES:
                    return True

            return False

        posible_actions = [
            (row, column)
            for row, column in adjacent_positions(*state)
            if not enemy_can_attack(row, column)
            and 0 <= row < BOARD_SIZE
            and 0 <= column < BOARD_SIZE
        ]

        return posible_actions

    def result(self, state, action):
        return action

    def cost(self, state, action, state2):
        return 1

    def print_state_representation(self, state):
        elements = {
            "K": [state],
            "X": ENEMIES,
        }
        print_grid(BOARD_SIZE, BOARD_SIZE, elements)


methods = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for search_method in methods:
    try_search_method(search_method, HnefataflProblem, INITIAL_STATE)
