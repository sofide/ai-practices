"""
Esta es una versión muy simplificada del juego Dota. En esta versión, el mapa es un
tablero de 3x3, participa un solo jugador, y tiene como objetivos derrotar a un héroe
enemigo y destruir su base en la menor cantidad de acciones posibles. El jugador
comienza en la esquina inferior izquierda del mapa, y en cada turno puede moverse a los
casilleros limítrofes (no en diagonal). Si se encuentra adyacente a un casillero de un
enemigo o edificio, también tiene disponible la acción de atacar a dicho objeto,
destruyéndolo como resultado. Dos objetos no pueden estar en la misma posición.

Al inicio del juego, el mapa y la distribución de objetos es la siguiente:
------+-----+-----+
|     |     | Be  |
------+-----+-----+    H = Héroe (jugador)
|     | He  |     |    He = Héroe enemigo
------+-----+-----+    Be = Base enemiga
|  H  |     |     |
------+-----+-----+

Ejemplo de acciones disponibles:
------+-----+-----+
|     |     | Be  |
------+-----+-----+
|  H  | He  |     |
------+-----+-----+
|     |     |     |
------+-----+-----+

En este estado, el héroe está junto al héroe enemigo. En esta situación puede moverse en
dos direcciones o atacar a He. Si ataca, en el estado resultante el héroe enemigo
estaría muerto.
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


# The initial state is definied as a tuple of three elements:
# - position of hero (player)
# - position of hero enemy (or None if they are dead)
# - position of enemy base (or None if it is destroyed)
INITIAL_STATE = ((2, 0), (1, 1), (0, 2))

ROWS = 3
COLUMNS = 3


class DotaProblem(SearchProblem):
    def is_goal(self, state):
        # The goal is to destroy all enemy heros and enemy bases
        _, enemy_hero, enemy_base = state

        return enemy_hero is None and enemy_base is None

    def actions(self, state):
        # all adjacent positions are valid actions.
        # If that position is empty, the action means "move to that position"
        # If it's not empty, the action means "attack that position"
        (hero_row, hero_column), _, _ = state

        posible_actions = [
            (hero_row - 1, hero_column),  # move up
            (hero_row + 1, hero_column),  # move down
            (hero_row, hero_column - 1),  # move left
            (hero_row, hero_column + 1),  # move right
        ]

        return [
            (row, column)
            for row, column in posible_actions
            if 0 <= row < ROWS
            and 0 <= column < COLUMNS
        ]


    def result(self, state, action):
        player_hero, enemy_hero, enemy_base = state

        # attack enemy base
        if enemy_base == action:
            return (player_hero, enemy_hero, None)

        # attack enemy hero
        if enemy_hero == action:
            return (player_hero, None, enemy_base)

        # move player hero
        return (action, enemy_hero, enemy_base)

    def cost(self, state, action, state2):
        return 1

    def print_state_representation(self, state):
        hero, enemy, base = state
        elements = {"H": [hero]}
        if enemy:
            elements["He"] = [enemy]
        if base:
            elements["Be"] = [base]

        print_grid(ROWS, COLUMNS, elements)


methods = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for search_method in methods:
    try_search_method(search_method, DotaProblem, INITIAL_STATE)
