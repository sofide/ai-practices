"""
El tour del Caballero
En el problema “Tour del Caballero” se trata de encontrar una secuencia de movimientos
de una sola pieza (caballo) en un tablero de ajedrez, de modo que se visiten todas las
casillas una sola vez. El “Caballero” puede comenzar en cualquier posición y hay que
moverse según las reglas normales para mover un caballo en el juego de ajedrez (en
forma de L).
"""
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    iterative_limited_depth_first,
)

from utils import print_grid, try_search_method

BOARD_SIZE = 8

HORSE_INITIAL_POSITION = (0, 0)

AVAILABLE_POSITIONS_IN_INITIAL_STATE = tuple(
    (row, column)
    for row in range(BOARD_SIZE)
    for column in range(BOARD_SIZE)
    if (row, column) != HORSE_INITIAL_POSITION
)

# A state is defined by a tuple of two elements:
# - The position of the horse
# - The available positions to visit
INITIAL_STATE = (HORSE_INITIAL_POSITION, AVAILABLE_POSITIONS_IN_INITIAL_STATE)


class CaballeroProblem(SearchProblem):
    def is_goal(self, state):
        _, available_positions = state
        return available_positions == ()

    def actions(self, state):
        (horse_row, horse_column), available_positions = state

        posible_movements = [
            (horse_row + 3, horse_column + 1),
            (horse_row + 3, horse_column - 1),
            (horse_row - 3, horse_column + 1),
            (horse_row - 3, horse_column - 1),
            (horse_row + 1, horse_column + 3),
            (horse_row + 1, horse_column - 3),
            (horse_row - 1, horse_column + 3),
            (horse_row - 1, horse_column - 3),
        ]

        posible_actions = [
            movement for movement in posible_movements
            if movement in available_positions
        ]

        return posible_actions

    def result(self, state, action):
        _, available_positions = state

        available_positions = list(available_positions)
        available_positions.remove(action)
        available_positions = tuple(available_positions)

        return (action, available_positions)

    def cost(self, state, action, state2):
        return 1

    def print_state_representation(self, state):
        horse, available_positions = state
        elements = {
            "C": horse,
            "X": available_positions,
        }
        print_grid(BOARD_SIZE, BOARD_SIZE, elements)


methods = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for search_method in methods:
    try_search_method(search_method, CaballeroProblem, INITIAL_STATE)
