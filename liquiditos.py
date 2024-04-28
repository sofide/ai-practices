"""
Resolviendo el juego de liquiditos "Sort Em All"
"""
from collections import defaultdict

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

# STATE: each tuple represents a tube
INITIAL_STATE_SIMPLE = (
    ("rojo", "rojo", "rojo", "verde"),
    ("verde", "verde", "verde", "rojo"),
    (None, None),
)

GOAL_TUBES_SIZE = 4  # in some level there can be smaller tubes that shouldn't be filled in the goal

ANY_COLOR = "any_color"



class LiquiditosProblem(SearchProblem):
    def is_goal(self, state):
        for tube in state:
            colors_in_tube = len(set(tube))
            if colors_in_tube > 1:
                #more than one color in tube, not a goal state
                return False
        return True

    def actions(self, state):
        # an action is defined by a tuple of two elements:
        # (origin_tube_index, receiver_tube)

        possible_origin_tubes = []
        possible_destination_tubes = []

        for tube_index, tube in enumerate(state):
            colors_in_tube = set(tube) # emptyness count as a color ("green", "green", None) == 2 colors

            if colors_in_tube == 1 and None in colors_in_tube:
                # empty tube can receive liquid of any color
                possible_destination_tubes.append((tube_index, ANY_COLOR))
                continue

            if colors_in_tube == 1 and len(tube) == GOAL_TUBES_SIZE:
                # this tube already reached the goal, cannot give or receive liquid
                continue

            top_color_index = 0
            top_color = tube[top_color_index]

            while top_color is None:
                top_color_index += 1
                top_color = tube[top_color_index]

            if None in tube:
                # this tube can receive liquid
                possible_destination_tubes.append((tube_index, top_color))

            # all tubes that are not goal or empty can be origin tubes

            possible_origin_tubes.append((tube_index, top_color))

            possible_actions = []
            for origin_index, origin_color in possible_origin_tubes:
                for destination_index, destination_color in possible_destination_tubes:
                    if origin_index != destination_index and destination_color in {origin_color, ANY_COLOR}:
                        possible_actions.append(origin_index, destination_index)

            return possible_actions

    def result(self, state, action):
        origin_index, destination_index = action
        origin_tube = list(state[origin_index])
        destination_tube = list(state[destination_index])

        # check which color is the liquid to transfer
        top_color_origin_index = 0
        color_to_transfer = origin_tube[top_color_origin_index]
        while color_to_transfer is None:
            top_color_origin_index += 1
            color_to_transfer = origin_tube[top_color_origin_index]

        # check how much liquid can be transfered
        next_color_index = top_color_origin_index + 1
        while next_color_index < len(origin_tube) and origin_tube[next_color_index] == color_to_transfer:
            next_color_index += 1

        how_much_liquid_can_give = next_color_index - top_color_origin_index
        how_much_liquid_can_receive = destination_tube.count(None)

        liquid_to_move = min(how_much_liquid_can_give, how_much_liquid_can_receive)

        # remove liquid from origin tube
        for slot_to_empty in range(top_color_origin_index, top_color_origin_index + liquid_to_move):
            origin_tube[slot_to_empty] = None

        # put liquid in destination tube
        first_slot_to_fill = how_much_liquid_can_receive - liquid_to_move
        for slot_to_fill in range(first_slot_to_fill, first_slot_to_fill + liquid_to_move):
            destination_tube[slot_to_fill] = color_to_transfer

        state[origin_index] = tuple(origin_tube)
        state[destination_index] = tuple(destination_tube)

        return tuple(state)

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        """
        For each tube the minimal pending moves are the quantity of mixed colours - 1
        """
        min_pending_moves = 0

        for tube in state:
            last_color = None
            mixed_colors_in_tube = 0

            for color in tube:
                if color != last_color:
                    mixed_colors_in_tube += 1

            if mixed_colors_in_tube:
                min_pending_moves += mixed_colors_in_tube -1

        return min_pending_moves

    def print_state_representation(self, state):
        tubes_quantity = len(state)
        max_tube_size = 0

        elements = defaultdict(list)

        for tube_index, tube in enumerate(state):
            tube_size = len(tube)
            if tube_size > max_tube_size:
                max_tube_size = tube_size

            for color_index, color in enumerate(tube):
                elements[color].append((tube_index, color_index))

        max_color_size = len(max(elements.keys, key=len))

        print_grid(rows=max_tube_size, columns=tubes_quantity, elements=elements, cell_size=max_color_size+2)


methods = (
    # breadth_first,
    # depth_first,
    # iterative_limited_depth_first,
    # uniform_cost,
    greedy,
    astar,
)

for search_method in methods:
    try_search_method(search_method, LiquiditosProblem, INITIAL_STATE_SIMPLE)
