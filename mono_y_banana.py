"""
Monos y bananas

El problema se trata de un mono en una habitación; algunas bananas cuelgan del techo y
el mono desgraciadamente no puede llegar a ellas. En la sala hay una silla con la
suficiente altura como para que si el mono se sube a ella pueda alcanzar las bananas.
El mono puede moverse, empujar la silla y/o subirse a ella. Por supuesto que el mono
quiere comer las bananas.

AYUDA: Se puede pensar que la habitación es muy estrecha (del tamaño de la silla), de
10 metros de largo, y los movimientos que realiza el mono son siempre iguales (50 cm).
"""
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    iterative_limited_depth_first,
)

from utils import print_grid, try_search_method

ROOM_SLOTS = 20  # 10 metros de habitación / 50 cm cada movimiento

BANANA_POSITION = 0

MONKEY_INITIAL_POSITION = 0
CHAIR_INITIAL_POSITION = 1

# a state is defined by two elements:
# - monkey position
# - chair position
INITIAL_STATE = (MONKEY_INITIAL_POSITION, CHAIR_INITIAL_POSITION)

class MonoProblem(SearchProblem):
    def is_goal(self, state):
        monkey, chair = state
        return monkey == chair == BANANA_POSITION

    def actions(self, state):
        # an action will be defined by two elementw:
        # - int: position to move
        # - boolean: push (push the chair) if it is false and the monkey moves to a
        # position where it is the chair, the monkey will climb the chair.
        monkey, chair = state

        posible_movements = [monkey + 1, monkey -1]
        movements = [
            (movement, False)
            for movement in posible_movements
            if 0 <= movement < ROOM_SLOTS
        ]

        if chair in posible_movements:
            movements.append((chair, True))

        return movements

    def result(self, state, action):
        monkey_before, chair = state
        monkey_now, push = action

        if push:
            direction = monkey_now - monkey_before
            chair_now = chair + direction
            return (monkey_now, chair_now)
        return (monkey_now, chair)

    def cost(self, state, action, action2):
        return 1

    def print_state_representation(self, state):
        monkey, chair = state
        elements = {
            "M": [(0, monkey)],
            "C": [(0, chair)],
            "B": [(0, BANANA_POSITION)],
        }
        print_grid(1, ROOM_SLOTS, elements)



methods = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for search_method in methods:
    try_search_method(search_method, MonoProblem, INITIAL_STATE)
