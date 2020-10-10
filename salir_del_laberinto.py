"""
La siguiente imagen representa la estructura de un laberinto. Se debe encontrar la
salida desde el casillero 1 hasta el 21.
"""
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    iterative_limited_depth_first,
)

from utils import try_search_method


TEMPLATE = """
------+-----+-----+-----+-----+-----+-----+
| 02                    |  03       |     |
|                                         |
---  -+-  --+-----+-  --+-----+  ---+ 04  +
| 05  | 06  | 07        | 08        |     |
|     |     |           |                 |
|           +-------  --+--  -+-----+     +
|     |     |  09       | 10  | 11  |     |
|     |                 |     |     |     |
-     +     +-  --+-  --+     +     +     +--------+
|     |     | 12  | 01  |     |     |              |
|     |     |           |           |        21    |
------+-----+     +-----+--  -+-----+     +        |
| 13  | 14  |     |  15       | 16  |     |        |
|                 |                 |     |--------+
-     +-----+--  -+--  -+-----+     +     +
|     | 17        |  18       |     |     |
|                 |           |     |     |
-     +----   ----+-----+-----+-  --+-----+
|     |  19       |   20                  |
|                                         |
------+-----+-----+-----+-----+-----+-----+
"""

DOORS = {
    1: [9, 12],
    2:  [5, 6, 7, 3],
    3:  [2, 8, 4],
    4:  [3, 8, 21],
    5:  [2, 6],
    6:  [5, 2, 9],
    7:  [2, 9],
    8:  [3, 4, 10],
    9:  [7, 6, 12, 1],
    10:  [8, 15, 11],
    11:  [10],
    12:  [9, 14, 17, 1],
    13:  [14, 17, 19],
    14:  [13, 12],
    15:  [10, 18, 16],
    16:  [15, 20],
    17:  [12, 13, 19],
    18:  [15],
    19:  [13, 17, 20],
    20:  [19, 16],
    21:  [4],
}

INITIAL_STATE = 1
GOAL_STATE = 21


class Laberinto(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE

    def actions(self, state):
        return tuple(DOORS[state])

    def result(self, state, action):
        return action

    def cost(self, state, action, state2):
        return 1

    def print_state_representation(self, state):
        state_str = str(state).rjust(2, '0')

        print(TEMPLATE.replace(state_str, "XX"))


methods = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for search_method in methods:
    try_search_method(search_method, Laberinto, INITIAL_STATE)
