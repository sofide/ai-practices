"""
Un grupo de 5 personas quiere cruzar un viejo y estrecho puente. Es una noche cerrada y
se necesita llevar una linterna para cruzar. El grupo sólo dispone de una linterna, a la
que le quedan 5 minutos de batería. Cada persona tarda en cruzar 10, 30, 60, 80 y 120
segundos, respectivamente. El puente sólo resiste un máximo de 2 personas cruzando a la
vez, y cuando cruzan dos personas juntas caminan a la velocidad del más lento. No se
puede lanzar la linterna de un extremo a otro del puente, así que cada vez que crucen
dos personas, alguien tiene que volver a cruzar hacia atrás con la linterna a buscar a
los compañeros que faltan, y así hasta que hayan cruzado todos.
"""
import math
from itertools import combinations

from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer

from utils import print_grid, try_search_method

TORCH_INITIAL_BATTERY = 5 * 60  # 5 minutes

ALL_PEOPLE = (10, 30, 60, 80, 120)

# STATE =  a tuple of three elements:
# - people in the left side of the bridge
# - people in the right side of the bridge
# - side of the bridge where is the torch (0=left, 1=right)
# - seconds remaining for the torch battery (just informative)
INITIAL_STATE = (ALL_PEOPLE, (), 0, TORCH_INITIAL_BATTERY)


class BridgeProblem(SearchProblem):
    def is_goal(self, state):
        # there aren't any remaining people on the left side of the bridge
        return state[0] == ()

    def actions(self, state):
        side_of_the_torch = state[2]
        people = state[side_of_the_torch]

        # each action is a tuple with the people who can be moved
        # one person movements
        actions = [(person,) for person in people ]

        # two people movements
        actions.extend(pair for pair in combinations(people, 2))

        posible_actions = []

        time = state[-1]
        for action in actions:
            time_with_action = time - max(action)

            if time_with_action >= 0:
                posible_actions.append(action)

        return posible_actions


    def result(self, state, action):
        left, right, torch_side, time = state

        if torch_side == 0:
            # when torch is in the left move pople to the right
            left = [person for person in left if person not in action]
            right = list(right)
            right.extend(action)

        else:
            # when torch is in the right move pople to the left
            left = list(left)
            left.extend(action)
            right = [person for person in right if person not in action]

        # move the torch to the other side
        final_torch_side = 0 if torch_side == 1 else 1

        time -= max(action)

        return (tuple(left), tuple(right), final_torch_side, time)


    def cost(self, state, action, state2):
        return max(action)

    def heuristic(self, state):
        left, right, torch_side, time = state

        if torch_side == 1:
            min_trips_from_left = len(left)
            min_trips_from_right = min_trips_from_left

        else:
            min_trips_from_left = len(left) - 1
            min_trips_from_right = min_trips_from_left - 1

        left_sorted = sorted(left, reverse=True)
        fastest = min(ALL_PEOPLE)
        second_fastest = min(p for p in ALL_PEOPLE if p != fastest)

        efficient_pairs_in_left = [
            left_sorted[position:position+2]
            for position in range(0, len(left_sorted), 2)
        ]

        min_left_cost = [max(pair) for pair in efficient_pairs_in_left]

        cost = sum(min_left_cost)
        # refill minimun trips from left with second_fastest time
        cost += (min_trips_from_left - len(efficient_pairs_in_left)) * second_fastest

        # the minimum value for trips from the right is the time for the fastest person
        cost += min_trips_from_right * fastest

        return cost

    def print_state_representation(self, state):
        cell_size = len(ALL_PEOPLE * 4) + 2
        cells = 5

        left, right, torch_side, time = state

        elements = {
            str(left): [(0, 0)],
            str(right): [(0, cells-1)],
            "T": [(0, 1) if torch_side == 0 else (0, cells - 2)],
            str(time): [(0, round(cells/2))],
        }

        print_grid(1, cells, elements, cell_size)


methods = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
    greedy,
    astar,
)

for search_method in methods:
    try_search_method(search_method, BridgeProblem, INITIAL_STATE)
