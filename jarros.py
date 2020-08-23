"""
Se tienen N jarros enumerados de 1 a N, donde la capacidad en litros del jarro I es I.
Esto es, el jarro 1 tiene capacidad de 1 litro, el jarro 2, 2 litros y así
sucesivamente.

Inicialmente el jarro N está lleno de agua y los demás están vacíos.

El objetivo es que todos los jarros queden con 1 litro de agua, teniendo como
operaciones permitidas trasvasar el contenido de un jarro a otro, operación que finaliza
al llenarse el jarro de destino o vaciarse el jarro de origen.

Todo esto se tiene que lograr con el menor costo posible, siendo I el costo de trasvasar
el contenido del jarro I a otro jarro.

En este caso concreto se tienen 4 jarros.
"""
from collections import defaultdict

from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    iterative_limited_depth_first,
)
from simpleai.search.viewers import BaseViewer

from utils import print_grid, try_search_method

VASES = 4
VASES_SIZE = (1, 2, 3, 4)

INITIAL_STATE = (0, 0, 0, 4)  # liters for each vase

GOAL_STATE = (1, 1, 1, 1)



class JarrosProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE

    def actions(self, state):
        # an action is defined by a tuple of two elements:
        # (origin_vase, receiver_vase)
        def is_full(vase):
            return state[vase] == VASES_SIZE[vase]

        vases_with_water = [
            vase_position
            for vase_position, vase_content in enumerate(state)
            if vase_content
        ]

        vases_not_full = [
            vase_position
            for vase_position, vase_content in enumerate(state)
            if vase_content < VASES_SIZE[vase_position]
        ]

        posible_actions = [
            (origin_vase, receiver_vase)
            for origin_vase in vases_with_water
            for receiver_vase in vases_not_full
            if origin_vase != receiver_vase
        ]

        return posible_actions

    def result(self, state, action):
        origin_vase, receiver_vase = action
        water_to_pour = min(
            state[origin_vase],
            VASES_SIZE[receiver_vase] - state[receiver_vase]
        )
        state = list(state)
        state[origin_vase] -= water_to_pour
        state[receiver_vase] += water_to_pour

        return tuple(state)

    def cost(self, state, action, state2):
        return 1

    def print_state_representation(self, state):
        elements = defaultdict(list)
        for vase_position, vase_content in enumerate(state):
            elements["X"*vase_content].append((0, vase_position))

        print_grid(1, VASES, elements, VASES)


methods = (
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

for search_method in methods:
    try_search_method(search_method, JarrosProblem, INITIAL_STATE)
